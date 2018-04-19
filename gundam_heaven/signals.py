from django.dispatch import Signal


def notify_follow(sender, **kwargs):
    new_kwargs = kwargs
    new_kwargs.pop('signal')
    comment = kwargs.get('comment', None)
    article = kwargs.get('article', None)
    owner = sender
    if isinstance(comment, int):
        new_kwargs['comment_id'] = new_kwargs.pop('comment')
    if isinstance(article, int):
        new_kwargs['article_id'] = new_kwargs.pop('article')
    owner.notifications.create(**new_kwargs)


signal_notification = Signal(providing_args=['subject', 'type', 'comment', 'article', 'verb'])
signal_notification.connect(notify_follow)