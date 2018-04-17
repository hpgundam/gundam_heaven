from gundam_heaven.models import Article
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required(login_url=reverse_lazy('gundam_heaven:login'))
@require_http_methods(['POST', 'GET'])
def post_article(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        article = request.user.articles.create(title=title, content=content)
        messages.success(request, 'successfully posted an article')
        return redirect(reverse('gundam_heaven:article-detail', kwargs={'pk': article.id}))
    elif request.method == 'GET':
        return render(request, 'gundam_heaven/post_article.html')

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'gundam_heaven/article_detail.html'
    context_object_name = 'article'
