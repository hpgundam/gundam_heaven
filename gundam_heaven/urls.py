from gundam_heaven import views, api
from django.urls import path, include
from rest_framework.routers import DefaultRouter

app_name = 'gundam_heaven'

account_urlpatterns = [
    path('register/', views.register, name='register'),
    path('<int:id>/', views.detail, name='show_user'),
    path('logout/', views.log_out, name='logout'),
    path('login/', views.log_in, name='login'),
    path('change_password/', views.change_password, name='change-password'),
    path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('change_photo/', views.change_photo, name='change-photo'),
    path('change_info/', views.change_info, name='change-info'),
    path('<int:id>/follow/', views.follow_user, name='follow-user'),
]

article_urlpatterns = [
    path('post/', views.post_article, name='post-article'),
    path('<int:pk>/', views.ArticleDetailView.as_view(), name='show_article'),
    path('<int:pk>/like/', views.like_article, name='like-article'),
    path('<int:pk>/comment/', views.comment_article, name='comment-article'),
    path('<int:article_pk>/comment/<int:comment_pk>/', views.get_full_chat, name='full-chat'),
]

notification_urlpatterns = [
    path('', views.NotificationListView.as_view(), name='notification-list'),
    path('read/', views.read_notification, name='read-notification'),
]

#api route
router = DefaultRouter()
router.register(r'users', api.UserViewSet)
router.register(r'userinfo', api.UserInfoViewSet)
router.register(r'userfollow', api.UserFollowViewSet)
router.register(r'articles', api.ArticleViewSet)
router.register(r'tags', api.TagViewSet)
router.register(r'mark', api.MarkViewSet)
router.register(r'comments', api.CommentViewSet)
router.register(r'notifications', api.NotificationViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('account/', include(account_urlpatterns)),
    path('article/', include(article_urlpatterns)),
    path('notification/', include(notification_urlpatterns)),
    path('api/', include(router.urls)),
]
