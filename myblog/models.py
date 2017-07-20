from __future__ import absolute_import
from django.db import models
from myauth.models import MyUser
from django.dispatch import receiver
from django.db.models.signals import post_save
from celery import Celery
from django.conf import settings
import os
import django

celery = Celery('tasks', broker='amqp://guest@localhost//') #!

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web95-92106107-phase3.settings')
django.setup()

app = Celery('web95-92106107-phase3')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# Create your models here.
DEFAULT_BLOG_ID = 1
class Blog(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default='', verbose_name="blog's name")
    author = models.ForeignKey(MyUser, related_name='blog')
    posts_words = models.CharField(max_length=1000, default='', blank=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, default='', verbose_name="post's title")
    summery = models.TextField(max_length=200)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    blog = models.ForeignKey(Blog, related_name='post', default=DEFAULT_BLOG_ID)

    def __str__(self):
        return self.title

DEFAULT_POST_ID = 1
class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=100)
    post = models.ForeignKey(Post, related_name='comment', default=DEFAULT_POST_ID)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

@celery.task()
def recalc(ID):
    blog = Blog.objects.get(id = ID)
    wordlist = []
    for post in blog.post.all():
        wordlist += post.text.split()

    wordfreq = [wordlist.count(w) for w in wordlist]
    blog.posts_words = ['word' + str(i + 1) + '-' + str(wordfreq[i]) for i in range(len(wordfreq))]

@receiver(post_save, sender=Post)
def posts_words_calc(sender, **kwargs):
    post = kwargs.get('instance')
    post.name = 'changed'
    id = post.blog.id
    recalc.delay(id)
