from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Blog(models.Model):
    title=models.CharField(max_length=50)
    text=models.TextField()
    date=models.DateTimeField(default=timezone.now)
    author=models.ForeignKey(User,on_delete=models.CASCADE)

class Comment(models.Model):
    blog=models.ForeignKey(Blog,on_delete=models.CASCADE, related_name='comments')
    name=models.CharField(max_length=80)
    text=models.TextField()
    date=models.DateTimeField(default=timezone.now)

class Like(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    blog=models.ForeignKey(Blog,on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

class Dislike(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    blog=models.ForeignKey(Blog,on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

class UrlHit(models.Model):
    url=models.URLField()
    hit=models.IntegerField(default=0)

    def increase(self):
        self.hit+=1
        self.save()

class HitCount(models.Model):
    url_hit=models.ForeignKey(UrlHit,on_delete=models.CASCADE)
    ip=models.CharField(max_length=40)
    session=models.CharField(max_length=40)
    date=models.DateTimeField(auto_now_add=True)