from gundam_heaven import views
from django.urls import path, include

app_name = 'gundam_heaven'

account_urlpatterns = [
    path('register/', views.register, name='register'),
    path('<int:id>/', views.detail, name='user-detail'),
    path('logout/', views.log_out, name='logout'),
    path('login/', views.log_in, name='login'),
    path('change_password/', views.change_password, name='password-change'),
    path('change_photo/', views.change_photo, name='change-photo'),
    path('change_info/', views.change_info, name='change-info'),
    path('<int:id>/follow/', views.follow_user, name='follow-user'), 
]

article_urlpatterns = [
    path('post/', views.post_article, name='post-article'),
    path('<int:pk>/', views.ArticleDetailView.as_view(), name='article-detail'),
]

urlpatterns = [
    path('', views.index, name='index'),
    path('account/', include(account_urlpatterns)),
    path('article/', include(article_urlpatterns)),
]

