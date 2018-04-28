from django.shortcuts import render
from django.contrib.auth.models import User
from gundam_heaven.models import Article
from gundam_heaven.utils import get_current_page
from django.db.models import Q

def index(request):
    cur_page_no = request.GET.get('page', 1)
    active_users = User.objects.order_by('-last_login')[:9]
    tag = request.GET.get('tag', None)
    if tag is not None:
        articles_total = Article.objects.filter(tags__name=tag).order_by('-update_time')
    else:
        articles_total = Article.objects.order_by('-update_time')
    keyword = request.GET.get('keyword', None)
    if keyword is not None:
        articles_total = articles_total.filter(Q(title__icontains=keyword)|Q(content__icontains=keyword))
    articles = get_current_page(articles_total, amt_per_page=2, cur_page_no=int(cur_page_no))
    return render(request, 'gundam_heaven/index.html', {'users': active_users, 'articles': articles})