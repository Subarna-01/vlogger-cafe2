from django.db import models


class UserSignUp(models.Model):
    user_id = models.CharField(primary_key=True,max_length=50)
    username = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=100)

class MasterVideoRecord(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.CharField(max_length=50,default=True)
    published_date = models.DateField(default=True)
    video_title = models.CharField(max_length=100)
    video_hashtags = models.CharField(max_length=100)
    video_desc = models.CharField(max_length=200)
    video_filename = models.FileField(upload_to="videos/",max_length=100)
    video_thumbnail = models.FileField(upload_to="thumbnails/",default=True)

class MyProfile(models.Model):
    user_id = models.CharField(max_length=50,default=True)
    myprofilepic = models.FileField(upload_to="profile-pic/",default=True)