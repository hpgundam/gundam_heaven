from django.shortcuts import render
from django.contrib.auth.models import User
from gundam_heaven.models import Article
from gundam_heaven.utils import get_current_page

def index(request):
    cur_page_no = request.GET.get('page', 1)
    active_users = User.objects.order_by('-last_login')[:9]
    articles_total = Article.objects.order_by('-update_time')
    articles = get_current_page(articles_total, amt_per_page=2, cur_page_no=int(cur_page_no))
    return render(request, 'gundam_heaven/index.html', {'users': active_users, 'articles': articles})