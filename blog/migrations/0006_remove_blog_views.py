# Generated by Django 2.2.6 on 2019-10-30 22:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_blog_views'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='views',
        ),
    ]
