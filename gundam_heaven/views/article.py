from gundam_heaven.models import Article, Tag, Mark, FavoriteFolder, ArticleFollow
from gundam_heaven.utils import get_current_page
from gundam_heaven.signals import signal_notification

from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Max, Q
from django.contrib.auth.mixins import LoginRequiredMixin


import json

@login_required(login_url=reverse_lazy('gundam_heaven:login'))
@require_http_methods(['POST', 'GET'])
def post_article(request):
    tags = Tag.objects.order_by('name')
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        selected_tags = request.POST.getlist('tags')
        try:
            article = request.user.articles.create(title=title, content=content)
            mark_list = []
            for tag_id in selected_tags:
                mark_list.append(Mark(article_id=article.id, tag_id=tag_id))
            Mark.objects.bulk_create(mark_list)
        except Exception as e:
            messages.error(request, 'post article failed.')
            return render(request, 'gundam_heaven/post_article.html', {'tags': tags, 'error': e.args[0]})
        messages.success(request, 'successfully posted an article')
        for follower in request.user.followers.all():
            signal_notification.send(follower.follower, subject=request.user, verb='posted an article', article=article, type=3)
        return redirect(reverse('gundam_heaven:show_article', kwargs={'pk': article.id}))
    elif request.method == 'GET':
        return render(request, 'gundam_heaven/post_article.html',{'tags': tags})

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'gundam_heaven/article_detail.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        followers = self.object.followers
        if followers is None or followers == '':
            like_amt = 0
        else:
            like_amt = len(followers.split(':'))
        context['like_amt'] = like_amt
        #get paginated comments
        context['comments'] = get_current_page(self.object.comments.order_by('-floor'), amt_per_page=3, cur_page_no=self.request.GET.get('page', 1))
        return context

@login_required(login_url=reverse_lazy('gundam_heaven:login'))
@require_POST
def like_article(request, pk):
    data = {}
    data['result'] = 'success'
    article = get_object_or_404(Article, id=pk)
    old_followers = article.followers
    visitor = request.POST['visitor']
    action = request.POST['action']
    if action == 'like':
        if old_followers is None or old_followers == '':
            new_followers = str(visitor)
            data['like_amt'] = 1
        else:
            old_followers_set = set(old_followers.split(':'))
            if visitor in old_followers_set:
                data['result'] = 'failure'
                data['error'] = 'already like'
                data['like_amt'] = len(old_followers_set)
                return HttpResponse(json.dumps(data), content_type='application/json')
            else:
                old_followers_set.add(visitor)
                new_followers = ':'.join(old_followers_set)
                data['like_amt'] = len(old_followers_set)
        article.followers = new_followers
        article.save()
        signal_notification.send(article.author, subject=request.user, verb='liked your article', article=article, type=1)
    elif action == 'unlike':
        if old_followers is None:
            data['result'] = 'failure'
            data['error'] = 'already unlike'
            data['like_amt'] = 0
        else:
            old_followers_set = set(old_followers.split(':'))
            if visitor not in old_followers_set:
                data['result'] = 'failure'
                data['error'] = 'already unlike'
                data['like_amt'] = len(old_followers_set)
            else:
                old_followers_set.remove(visitor)
                new_followers = ':'.join(old_followers_set)
                article.followers = new_followers
                article.save()
                data['like_amt'] = len(old_followers_set)
        signal_notification.send(article.author, subject=request.user, verb='unliked your article', article=article, type=1)
    else:
        data['result'] = 'failure'
        data['error'] = 'invalid action'
    return HttpResponse(json.dumps(data), content_type='application/json')

@login_required(login_url=reverse_lazy('gundam_heaven:login'))
@require_POST
def comment_article(request, pk):
    content = request.POST['comment']
    article = get_object_or_404(Article, id=pk)
    max_floor = article.comments.all().aggregate(Max('floor'))['floor__max'] or 0
    reply_to = request.POST.get('reply_to', None)
    if reply_to is None:
        request.user.commenting.create(article=article, reply_to=reply_to, content=content, floor=max_floor+1)
        signal_notification.send(article.author, subject=request.user, verb='commented', article=article, type=2)
    else:
        request.user.commenting.create(article=article, reply_to_id=int(reply_to), content=content, floor=max_floor + 1)
        signal_notification.send(article.author, subject=request.user, verb='commented your comment', comment=int(reply_to), article=article, type=2)
    return redirect(reverse('gundam_heaven:show_article', kwargs={'pk': article.id}))

@require_GET
def get_full_chat(request, article_pk, comment_pk):
    cur_page_no = request.GET.get('page', 1)
    article = get_object_or_404(Article, id=article_pk)
    comments_all = article.comments.filter(Q(id=comment_pk)|Q(reply_to_id=comment_pk)).order_by('floor')
    comments = get_current_page(comments_all, amt_per_page=3, cur_page_no=cur_page_no)
    return render(request, 'gundam_heaven/comment_full_chat.html', {'comments': comments, 'article': article})

@login_required(login_url=reverse_lazy('gundam_heaven:login'))
def add_article_to_favorite(request, article_pk):
    if request.method == 'POST':
        folder_id = request.POST.get('folder', None)
        if folder_id is not None:
            folder = get_object_or_404(FavoriteFolder, id=folder_id)
        else:
            folder = request.user.favoritefolder_set.create(name='Default')
        article = get_object_or_404(Article, id=article_pk)
        ArticleFollow.objects.create(article=article, folder=folder)
        return redirect(reverse('gundam_heaven:show_article', kwargs={'pk': article_pk}))
    elif request.method == 'GET':
        folders = request.user.favoritefolder_set.all()
        return render(request, 'gundam_heaven/select_folder.html', {'folders': folders, 'article_id': article_pk})

@login_required(login_url=reverse_lazy('gundam_heaven:login'))
@require_POST
def add_favorite_folder(request):
    data = {}
    try:
        request.user.favoritefolder_set.create(name=request.POST['folder_name'])
    except Exception as e:
        data['result'] = 'failure'
        data['error'] = e.args[0]
        print(e)
    else:
        data['result'] = 'success'
        data['name'] = request.POST['folder_name']
    return HttpResponse(json.dumps(data), content_type='application/json')





