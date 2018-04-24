from django.db import models

# Create your models here.
from django.contrib.auth.models import User

User = User

SEX_CHOICES = (
    (0, 'Female'),
    (1, 'Male'),
    (9, 'Secret')
)

def user_dir(instance, filename):
    return 'photo/{}/{}'.format(instance.owner.id, filename)

class UserInfo(models.Model):
    nickname = models.CharField(max_length=150)
    age = models.PositiveIntegerField(default=17)
    sex = models.IntegerField(choices=SEX_CHOICES, default=9)
    photo = models.ImageField(upload_to=user_dir, default='photo/default.jpg', blank=True)
    owner = models.OneToOneField(User, on_delete=models.CASCADE)

    def __repr__(self):
        return '<UserInfo: {}>'.format(self.nickname)

    def __str__(self):
        return self.__repr__()


class UserFollow(models.Model):
    follower = models.ForeignKey(User, on_delete=True, related_name='followees')
    followee = models.ForeignKey(User, on_delete=True, related_name='followers')

    class Meta:
        unique_together = ('follower', 'followee')

    def __repr__(self):
        return '<{} follows {}>'.format(self.follower.userinfo.nickname, self.followee.userinfo.nickname)

    def __str__(self):
        return self.__repr__()

class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=True, related_name='articles')
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    followers = models.TextField(null=True, blank=True)

    def __repr__(self):
        return '<Article: {}>'.format(self.title)

    def __str__(self):
        return self.__repr__()

    class Meta:
        ordering = ('-update_time', )


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    articles = models.ManyToManyField(Article, through='Mark', related_name='tags')

    def __repr__(self):
        return '<Tag: {}>'.format(self.name)

    def __str__(self):
        return self.__repr__()

class Mark(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    def __repr__(self):
        return '<{} marks {}>'.format(self.article.title, self.tag.name)

    def __str__(self):
        return self.__repr__()

    class Meta:
        unique_together = ('article', 'tag')

class Comment(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commenting')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    reply_to = models.ForeignKey('self', on_delete=models.CASCADE, related_name='reply_from', blank=True, null=True)
    floor = models.PositiveIntegerField()
    content = models.TextField(max_length=100)
    create_time = models.DateTimeField(auto_now=True)

NOTIFICATION_TYPES = (
    (1, 'like_follow'),
    (2, 'comment_article'),
    (3, 'followee_event'),
)

class Notification(models.Model):
    type = models.PositiveIntegerField(choices=NOTIFICATION_TYPES)
    subject = models.ForeignKey(User, on_delete=models.CASCADE)
    verb = models.CharField(max_length=100)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, blank=True, null=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, blank=True, null=True)
    create_time = models.DateTimeField(auto_now=True)
    has_read = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')

    class Meta:
        ordering = ('has_read', '-create_time')


class FavoriteFolder(models.Model):
    name = models.CharField(max_length=100)
    create_time = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    articles = models.ManyToManyField(Article, through='ArticleFollow')

    class Meta:
        unique_together = (('name', 'owner'), )
        ordering = ['-create_time']


class ArticleFollow(models.Model):
    folder = models.ForeignKey(FavoriteFolder, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('folder', 'article')


