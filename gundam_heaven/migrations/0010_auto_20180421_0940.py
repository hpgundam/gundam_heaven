# Generated by Django 2.0.4 on 2018-04-21 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gundam_heaven', '0009_auto_20180419_0926'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notification',
            options={'ordering': ('has_read', '-create_time')},
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='commentor',
            new_name='commenter',
        ),
        migrations.AlterField(
            model_name='notification',
            name='type',
            field=models.PositiveIntegerField(choices=[(1, 'like_follow'), (2, 'comment_article'), (3, 'followee_event')]),
        ),
    ]
