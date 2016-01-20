from django.db import models

# Create your models here.

class Posts(models.Model):
    posdtid = models.CharField(max_length=200)
    postinfo = models.CharField(max_length=100, default='no')


class PostInfo(models.Model):
    postid = models.ForeignKey(Posts) 
    user = models.OneToOneField(User)
    title = models.CharField(max_length=1000L)
    youtube_url = models.CharField(max_length=1000L, null=True, unique=True)
    youtube_title = models.CharField(max_length=1000L)
    
    facebook_url = models.CharField(max_length=1000L, null=True, unique=True)
    facebook_title = models.CharField(max_length=1000L)
    branded_revenue = models.IntegerField(default=0)
    production_cost = models.IntegerField(default=0)
    


    
