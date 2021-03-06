# Generated by Django 2.0.4 on 2018-04-19 09:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gundam_heaven', '0008_auto_20180419_0908'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='article',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gundam_heaven.Article'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gundam_heaven.Comment'),
        ),
    ]
