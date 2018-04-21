from rest_framework import serializers
from gundam_heaven import models
from django.contrib.auth.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='gundam_heaven:user-detail')
    info = serializers.HyperlinkedIdentityField(view_name='gundam_heaven:userinfo-detail')
    followers = serializers.HyperlinkedIdentityField(many=True, view_name='gundam_heaven:userfollow-detail')
    followees = serializers.HyperlinkedIdentityField(many=True, view_name='gundam_heaven:userfollow-detail')

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'password', 'email', 'last_login', 'date_joined',
                  'is_superuser', 'is_staff', 'info', 'followers', 'followees')

class UserInfoSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='gundam_heaven:userinfo-detail')
    owner = serializers.HyperlinkedRelatedField(view_name='gundam_heaven:user-detail', read_only=True)

    class Meta:
        model = models.UserInfo
        fields = ('url', 'id', 'nickname', 'age', 'sex', 'photo', 'owner')


class UserFollowSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='gundam_heaven:userfollow-detail')
    follower = serializers.HyperlinkedRelatedField(view_name='gundam_heaven:user-detail', read_only=True)
    followee = serializers.HyperlinkedRelatedField(view_name='gundam_heaven:user-detail', read_only=True)

    class Meta:
        model = models.UserFollow
        fields = ('url', 'id', 'follower', 'followee')


class AritcleSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='gundam_heaven:article-detail')
    author = serializers.HyperlinkedRelatedField(view_name='gundam_heaven:user-detail', read_only=True)
    tags = serializers.HyperlinkedRelatedField(many=True, view_name='gundam_heaven:tag-detail', read_only=True)

    class Meta:
        model = models.Article
        fields = ('url', 'id', 'title', 'author', 'create_time', 'update_time', 'followers' , 'tags', 'content')

class MarkSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='gundam_heaven:mark-detail')
    article = serializers.HyperlinkedRelatedField(view_name='gundam_heaven:article-detail', read_only=True)
    tag = serializers.HyperlinkedRelatedField(view_name='gundam_heaven:tag-detail', read_only=True)
    class Meta:
        model = models.Mark
        fields = ('url', 'id', 'article', 'tag')

class TagSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='gundam_heaven:tag-detail')
    articles = serializers.HyperlinkedRelatedField(many=True, view_name='gundam_heaven:article-detail', read_only=True)
    class Meta:
        model = models.Tag
        fields = ('url', 'id', 'name', 'articles')


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='gundam_heaven:comment-detail')
    commenter = serializers.HyperlinkedRelatedField(view_name='gundam_heaven:user-detail', read_only=True)
    article = serializers.HyperlinkedRelatedField(view_name='gundam_heaven:article-detail', read_only=True)
    reply_to = serializers.HyperlinkedRelatedField(view_name='gundam_heaven:comment-detail', read_only=True)

    class Meta:
        model = models.Comment
        fields = ('url', 'id', 'commenter', 'article', 'reply_to', 'floor', 'create_time', 'content')


class NotificationSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='gundam_heaven:notification-detail')
    subject = serializers.HyperlinkedRelatedField(view_name='gundam_heaven:user-detail', read_only=True)
    article = serializers.HyperlinkedRelatedField(view_name='gundam_heaven:article-detail', read_only=True)
    comment = serializers.HyperlinkedRelatedField(view_name='gundam_heaven:comment-detail', read_only=True)
    owner = serializers.HyperlinkedRelatedField(view_name='gundam_heaven:user-detail', read_only=True)

    class Meta:
        model = models.Notification
        fields = ['url', 'id', 'subject', 'verb', 'article', 'comment', 'create_time', 'has_read', 'owner']






