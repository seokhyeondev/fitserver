from django.db import models
import uuid
from django.db import models
from django.contrib.postgres.fields import ArrayField
# Create your models here.

class HotKeyword(models.Model):
    word = models.CharField(max_length=40, blank=False, default='')
    nowCount = models.IntegerField(default=0)
    prevCount = models.IntegerField(default=0)
        
class UserSearchLog(models.Model):
    email = models.EmailField(max_length=40, blank=False, default='')
    word = models.CharField(max_length=40, blank=False, default='')
    date = models.DateField(auto_now=True)
    
class Garment(models.Model):
    uuid = models.CharField(max_length=100, blank=True, default='')
    image = models.CharField(max_length=500, blank=True, default='')
    color = models.CharField(max_length=20, blank=True, default='')
    category = models.CharField(max_length=40, blank=True, default='')
    tags = ArrayField(models.CharField(max_length=40, blank=True, null=True, default=''), blank=True, null=True)
    
class UserOutfit(models.Model):
    top = models.ForeignKey(Garment, related_name='top', on_delete=models.DO_NOTHING, db_constraint=False, blank=True, null=True)
    bottom = models.ForeignKey(Garment, related_name='bottom', on_delete=models.DO_NOTHING, db_constraint=False, blank=True, null=True)
    dress = models.ForeignKey(Garment, related_name='dress', on_delete=models.DO_NOTHING, db_constraint=False, blank=True, null=True)
    outer = models.ForeignKey(Garment, related_name='outer', on_delete=models.DO_NOTHING, db_constraint=False, blank=True, null=True)
    shoes = models.ForeignKey(Garment, related_name='shoes', on_delete=models.DO_NOTHING, db_constraint=False, blank=True, null=True)
    hash_tag = models.CharField(max_length=400, blank=False, null=True)
    comment = models.CharField(max_length=400, blank=False, null=True)
    
class Feed(models.Model):
    email = models.EmailField(max_length=50, blank=False)
    nickname = models.CharField(max_length=12, blank=False)
    like_log_id = models.IntegerField(default=0, blank=False)
    isShow = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    user_outfit = models.ForeignKey(UserOutfit, related_name='user_outfit', on_delete=models.DO_NOTHING, db_constraint=False)
    style_tag = ArrayField(models.CharField(max_length=40, blank=False, default=''), blank=True, null=True)
