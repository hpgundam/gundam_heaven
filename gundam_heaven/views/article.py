from gundam_heaven.models import Article, Tag, Mark
from gundam_heaven.utils import get_current_page

from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.decorators.http import require_http_methods, require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Max

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
        return redirect(reverse('gundam_heaven:article-detail', kwargs={'pk': article.id}))
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
    commentee = request.POST.get('commentee', None)
    if commentee is None:
        request.user.commenting.create(article=article, commentee=commentee, content=content, floor=max_floor+1)
    else:
        request.user.commenting.create(article=article, commentee_id=int(commentee), content=content, floor=max_floor + 1)
    return redirect(reverse('gundam_heaven:article-detail', kwargs={'pk': article.id}))



