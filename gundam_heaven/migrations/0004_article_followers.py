# Generated by Django 2.0.4 on 2018-04-18 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gundam_heaven', '0003_auto_20180417_1357'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='followers',
            field=models.TextField(blank=True, null=True),
        ),
    ]