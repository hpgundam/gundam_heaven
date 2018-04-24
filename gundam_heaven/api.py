from gundam_heaven import serializers
from gundam_heaven.permissions import IsOwnerOrReadOnly
from gundam_heaven import models

from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from rest_framework.exceptions import APIException

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http.response import Http404
from django.db.models import Q


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


class UserInfoViewSet(ModelViewSet):
    queryset = models.UserInfo.objects.all()
    serializer_class = serializers.UserInfoSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


class UserFollowViewSet(ModelViewSet):
    queryset = models.UserFollow.objects.all()
    serializer_class = serializers.UserFollowSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        follower_id = self.request.data['follower_id']
        followee_id = self.request.data['followee_id']
        try:
            follower = get_object_or_404(User, id=follower_id)
        except Http404:
            raise APIException(detail='follower does not exist')
        try:
            followee = get_object_or_404(User, id=followee_id)
        except Http404:
            raise APIException(detail='followee does not exist')
        if follower_id != followee_id:
            serializer.save(follower=follower, followee=followee)
        else:
            raise APIException(detail='users can not follow themselves.')


class ArticleViewSet(ModelViewSet):
    queryset = models.Article.objects.all()
    serializer_class = serializers.AritcleSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def get_queryset(self):
        query_set = super().get_queryset()
        filters = {}
        tag = self.request.GET.get('tag', None)
        if tag is not None:
            filters['tags__name'] = tag
        author = self.request.GET.get('author', None)
        if author is not None:
            filters['author__userinfo__nickname'] = author
        return query_set.filter(**filters)




class TagViewSet(ModelViewSet):
    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class MarkViewSet(ModelViewSet):
    queryset = models.Mark.objects.all()
    serializer_class = serializers.MarkSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        article_id = self.request.data['article_id']
        tag_id = self.request.data['tag_id']
        try:
            article = get_object_or_404(models.Article, id=article_id)
        except Http404:
            raise APIException(detail='article does not exist')
        try:
            tag = get_object_or_404(models.Tag, id=tag_id)
        except Http404:
            raise APIException(detail='tag does not exist')
        serializer.save(article=article, tag=tag)


class CommentViewSet(ModelViewSet):
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


class NotificationViewSet(ModelViewSet):
    queryset = models.Notification.objects.all()
    serializer_class = serializers.NotificationSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)



