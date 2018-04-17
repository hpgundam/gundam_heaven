from django.shortcuts import render
from django.contrib.auth.models import User
from gundam_heaven.models import Article

def index(request):
    active_users = User.objects.order_by('-last_login')[:9]
    articles = Article.objects.order_by('-update_time')
    return render(request, 'gundam_heaven/index.html', {'users': active_users, 'articles': articles})