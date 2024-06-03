from django import forms
from client.models import MasterVideoRecord,UserSignUp,MyProfile

class FileUpload(forms.ModelForm):
    class Meta:
        model = MasterVideoRecord
        fields = ["video_title","video_hashtags","video_desc","video_filename","video_thumbnail"]
        widgets = {
            "video_title": forms.TextInput(attrs={"id": "videotitle","class": "form-control bg-dark text-light","name": "videotitle","placeholder": "Add a video title"}),
            "video_hashtags": forms.TextInput(attrs={"id": "videohashtags","class": "form-control bg-dark text-light","name": "videohashtags","placeholder": "Add hash tags (like #trending,#latest)"}),
            "video_desc": forms.Textarea(attrs={"id": "videodesc","class": "form-control bg-dark text-light","name": "videodesc","placeholder": "Add a description","rows": 5}),
            "video_filename": forms.FileInput(attrs={"id": "videofilename","class": "form-control bg-dark text-light","name": "videofilename"}),
            "video_thumbnail": forms.FileInput(attrs={"id": "videothumbnail","class": "form-control bg-dark text-light","name": "videothumbnail"}),
        }
class SignUp(forms.ModelForm):
    class Meta:
        model = UserSignUp
        fields = ["username","email","password"]
        widgets = {
            "username": forms.TextInput(attrs={"id": "uname","class": "form-control bg-dark text-light","name": "uname","placeholder": "Username"}),
            "email": forms.EmailInput(attrs={"id": "uemail","class": "form-control bg-dark text-light","name": "uemail","placeholder": "Email Address"}),
            "password": forms.PasswordInput(attrs={"id": "upass1","class": "form-control bg-dark text-light","name": "upass1","placeholder": "Password"}),
        }

class SignIn(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"id": "uname","class": "form-control bg-dark text-light","name": "uname","placeholder": "Username"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"id": "upass","class": "form-control bg-dark text-light","name": "upass","placeholder": "Password"}))

class MyProfileSettings(forms.ModelForm):
    class Meta:
        model = MyProfile
        fields = ["myprofilepic"]
        widgets = {
             "myprofilepic": forms.FileInput(attrs={"id": "myprofilepic","class": "form-control bg-dark text-light","name": "myprofilepic"}),
        }

class Search(forms.Form):
    search_query = forms.CharField(widget=forms.TextInput(attrs={
        "id": "search","class": "bg-dark text-light","name": "search","placeholder": "Search..."
    }))