from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetView as PRV, \
    PasswordResetConfirmView as PRConV, PasswordResetDoneView as PRDV, \
    PasswordResetCompleteView as PRComV
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from django.http import HttpResponse

from django.conf import settings
import os
import glob
import json

from gundam_heaven.models import UserInfo
from gundam_heaven.forms import FileUploadForm
from gundam_heaven.utils import get_current_page

from gundam_heaven.signals import signal_notification

from django.core.exceptions import ObjectDoesNotExist

@require_http_methods(['GET', 'POST'])
def register(request):
    '''
    validate form data
    create user object
    login user
    flash messages
    '''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            UserInfo.objects.create(nickname=form.cleaned_data['username'], owner=form.instance)
            login(request, form.instance)
            messages.success(request, 'successfully registered.')
            return redirect(reverse('gundam_heaven:user-detail', kwargs={'id': form.instance.id}))
        else:
            messages.error(request, 'register failed.')
            return render(request, 'gundam_heaven/register.html', {'form': form, 'action': reverse_lazy('gundam_heaven:register')})
    elif request.method == 'GET':
        form = UserCreationForm()
        return render(request, 'gundam_heaven/register.html', {'form': form, 'action': reverse_lazy('gundam_heaven:register')})

@require_GET
def detail(request, id):
    cur_page_no = request.GET.get('page', 1)
    user = get_object_or_404(User, id=id)
    title = 'Home Page of {}'.format(user.username)
    followers = [ follower.follower for follower in user.followers.all() ]
    followees = [ followee.followee for followee in user.followees.all() ]
    articles_all = user.articles.order_by('-update_time')
    articles = get_current_page(articles_all, amt_per_page=1, cur_page_no=int(cur_page_no))
    return render(request, 'gundam_heaven/user_detail.html', {'owner': user, 'title': title, 'followers': followers, 'followees': followees, 'articles': articles})

@require_http_methods(['GET', 'POST'])
def log_in(request):
    redirect_to = request.POST.get('next', request.GET.get('next', None))
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.user_cache)
            messages.success(request, 'successfully logged in')
            if redirect_to is not None:
                return  redirect(redirect_to)
            else:
                return redirect(reverse('gundam_heaven:user-detail', kwargs={'id': form.user_cache.id}))
        else:
            messages.error(request, 'log in failed.')
            return render(request, 'gundam_heaven/login.html', {'form': form, 'action': reverse_lazy('gundam_heaven:login'), 'next': redirect_to})
    elif request.method == 'GET':
        form = AuthenticationForm()
        return render(request, 'gundam_heaven/login.html', {'form': form, 'action': reverse_lazy('gundam_heaven:login'), 'next': redirect_to})

@login_required(login_url=reverse_lazy('gundam_heaven:login'))
def log_out(request):
    logout(request)
    messages.success(request, 'sucessfully logged out')
    return redirect(reverse('gundam_heaven:index'))

@login_required(login_url=reverse_lazy('gundam_heaven:login'))
@require_http_methods(['GET', 'POST'])
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'successfully changed your password')
            login(request, request.user)
            return redirect(reverse('gundam_heaven:user-detail', kwargs={'id': request.user.id}))
        else:
            return render(request, 'gundam_heaven/change_password.html', {'form': form, 'action': reverse_lazy('gundam_heaven:password-change')})
    elif request.method == 'GET':
        form = PasswordChangeForm(request.user)
        return render(request, 'gundam_heaven/change_password.html', {'form': form, 'action': reverse_lazy('gundam_heaven:password-change')})

@login_required(login_url=reverse_lazy('gundam_heaven:login'))
@require_http_methods(['GET', 'POST'])
def change_photo(request):
    default_photos_dir = os.path.join(settings.MEDIA_ROOT, 'photo', '0', '*')
    default_photos_path = glob.glob(default_photos_dir)
    default_photos_url = [os.path.sep+os.path.join('media', 'photo', '0', os.path.basename(path))  for path in default_photos_path]
    if request.method == 'POST':
        try:
            userinfo = request.user.userinfo
        except ObjectDoesNotExist :
            user = request.user
            userinfo = UserInfo(nickname=user.username, owner=user)
        form = FileUploadForm(data=request.POST, files=request.FILES, instance=userinfo)
        if len(request.FILES) == 0:
            photo = request.POST.getlist('photo')
            if photo[0] == '':
                messages.error(request, 'Please at least choose one way.')
                return render(request, 'gundam_heaven/upload_photo.html',
                              {'form': form, 'default_photos': default_photos_url})
            userinfo.photo = request.POST.getlist('photo')[0].lstrip(os.path.sep+os.path.basename(settings.MEDIA_ROOT)+os.path.sep)
            userinfo.save()
            messages.success(request, 'successfully changed your photo')
            return redirect(reverse('gundam_heaven:user-detail', kwargs={'id': request.user.id}))
        if form.is_valid():
            form.save()
            messages.success(request, 'successfully changed your photo')
            return redirect(reverse('gundam_heaven:user-detail', kwargs={'id': request.user.id}))
        else:
            messages.error(request, 'upload file failed')
            return render(request, 'gundam_heaven/upload_photo.html', {'form': form, 'default_photos': default_photos_url})
    elif request.method == 'GET':
        form = FileUploadForm()
        return render(request, 'gundam_heaven/upload_photo.html', {'form': form, 'default_photos': default_photos_url})

@login_required(login_url=reverse_lazy('gundam_heaven:login'))
@require_http_methods(['GET', 'POST'])
def change_info(request):
    context = {}
    user = request.user
    try:
        userinfo = user.userinfo
    except ObjectDoesNotExist:
        userinfo = UserInfo(nickname=user.username, owner=user)
    context['nickname'] = userinfo.nickname
    context['age'] = userinfo.age
    context['sex'] = userinfo.sex
    context['email'] = user.email
    if request.method == 'POST':
        # form = UserInfoChangeForm(request.POST)
        # if form.is_valid():
            # user.email = form.cleaned_data['email']
            # userinfo.nickname = form.cleaned_data['nickname']
            # userinfo.age = form.cleaned_data['age']
            # userinfo.sex = form.cleaned_data['sex']
        email = request.POST['email']
        nickname = request.POST['nickname']
        age = int(request.POST['age'])
        sex = int(request.POST['sex'])
        try:
            user.email = email
            userinfo.nickname = nickname
            userinfo.age = age
            userinfo.sex = sex
            user.save()
            userinfo.save()
            messages.success(request, 'successfully changed your information')
            return redirect(reverse('gundam_heaven:user-detail', kwargs={'id': request.user.id}))
        except Exception as e:
        # else:
            context['action'] = reverse_lazy('gundam_heaven:change-info')
            return render(request, 'gundam_heaven/change_userinfo.html', context)
    elif request.method == 'GET':
        # form = UserInfoChangeForm()
        context['action'] = reverse_lazy('gundam_heaven:change-info')
        return render(request, 'gundam_heaven/change_userinfo.html', context)

@login_required(login_url=reverse_lazy('gundam_heaven:login'))
@require_POST
def follow_user(request, id):
    data = {}
    action = request.POST['action']
    followee = get_object_or_404(User, id=id)
    follower = request.user
    if action == 'follow':
        try:
            follower.followees.create(followee=followee)
        except Exception as e:
            data['result'] = 'failure'
            data['error'] = e.args[0]
            raise e
        else:
            data['result'] = 'success'
            data['message'] = "You've successfully followed {}".format(followee.userinfo.nickname)
            signal_notification.send(followee, subject=follower, verb='followed you', type=1)
    elif action == 'unfollow':
        try:
            follower.followees.get(followee=followee).delete()
        except Exception as e:
            data['result'] = 'failure'
            data['error'] = e.args[0]
            raise e
        else:
            data['result'] = 'success'
            data['message'] = "You've successfully unfollowed {}".format(followee.userinfo.nickname)
            signal_notification.send(followee, subject=follower, verb='unfollowed you', type=1)
    else:
        data['result'] = 'failure'
        data['error'] = 'invalid action'
    return HttpResponse(json.dumps(data), content_type="application/json")

class PasswordResetView(LoginRequiredMixin, PRV):
    email_template_name = 'gundam_heaven/registration/password_reset_email.html'
    subject_template_name = 'gundam_heaven/registration/password_reset_subject.txt'
    success_url = reverse_lazy('gundam_heaven:password_reset_done')
    template_name = 'gundam_heaven/registration/password_reset_form.html'
    login_url = reverse_lazy('gundam_heaven:login')

class PasswordResetConfirmView(LoginRequiredMixin, PRConV):
    template_name = 'gundam_heaven/registration/password_reset_confirm.html'
    success_url = reverse_lazy('gundam_heaven:password_reset_complete')
    login_url = reverse_lazy('gundam_heaven:login')

class PasswordResetDoneView(PRDV):
    template_name = 'gundam_heaven/registration/password_reset_done.html'

class PasswordResetCompleteView(PRComV):
    template_name = 'gundam_heaven/registration/password_reset_complete.html'





