from django.db import models

# Create your models here.
from django.contrib.auth.models import User


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

    def __repr__(self):
        return '<Article: {}'.format(self.title)

    def __str__(self):
        return self.__repr__()


