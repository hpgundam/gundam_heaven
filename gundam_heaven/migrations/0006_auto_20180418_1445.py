# Generated by Django 2.0.4 on 2018-04-18 14:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gundam_heaven', '0005_auto_20180418_1028'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('floor', models.PositiveIntegerField()),
                ('content', models.TextField()),
                ('create_time', models.DateTimeField(auto_now=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='gundam_heaven.Article')),
                ('commentee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='commented', to=settings.AUTH_USER_MODEL)),
                ('commentor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commentting', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
