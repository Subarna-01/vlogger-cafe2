from django.contrib import admin
from client.models import MasterVideoRecord,UserSignUp,MyProfile

@admin.register(MasterVideoRecord)
class MasterVideoRecord(admin.ModelAdmin):
    list_display = ("user_id","video_title","video_hashtags","video_desc","video_filename","published_date")

@admin.register(UserSignUp)
class UserSignUp(admin.ModelAdmin):
    list_display = ("user_id","username","email","password")

@admin.register(MyProfile)
class MyProfile(admin.ModelAdmin):
    list_display = ("user_id","myprofilepic")
