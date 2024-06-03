from django.shortcuts import render
from ipware import get_client_ip
import requests
import json
import uuid
import hashlib
from client.forms import FileUpload,SignUp,SignIn,MyProfileSettings,Search
from client.models import MasterVideoRecord,UserSignUp,MyProfile
from django.http import HttpResponseRedirect
from datetime import date

def getIndex(request):
    profile_settings = None
    loc = getClientLoc(request)
    video_records = MasterVideoRecord.objects.raw("SELECT * FROM client_usersignup INNER JOIN client_mastervideorecord ON client_usersignup.user_id = client_mastervideorecord.user_id")
    try:
        profile_settings = MyProfile.objects.filter(user_id=request.session["user_id"])
    except Exception:
        pass
    session_info = {"user_id": request.session.get("user_id"),"username": request.session.get("username")}

    if request.method == "POST":
        fm = Search(request.POST)
        if fm.is_valid():
            search_query = fm.cleaned_data["search_query"]
            search_result = MasterVideoRecord.objects.raw("SELECT * FROM client_usersignup INNER JOIN client_mastervideorecord ON client_usersignup.user_id = client_mastervideorecord.user_id WHERE client_mastervideorecord.video_title LIKE '%{query}%' OR client_mastervideorecord.video_hashtags LIKE '%{query}%' OR client_mastervideorecord.video_desc LIKE '%{query}%'".format(query = search_query)) 
            return render(request,"index.html",{"location": loc,"video_records": search_result,"session": session_info,"profile_settings": profile_settings,"form": fm})
            
    fm = Search()

    return render(request,"index.html",{"location": loc,"video_records": video_records,"session": session_info,"profile_settings": profile_settings,"form": fm})

def getProfile(request):
    loc = getClientLoc(request)
    if "user_id" not in request.session and "username" not in request.session:
        return HttpResponseRedirect("/vloggercafe/signin/")
    else:
        session_info = {"user_id": request.session.get("user_id"),"username": request.session.get("username")}
        
        video_record = MasterVideoRecord.objects.filter(user_id=request.session["user_id"])
        profile_settings = MyProfile.objects.filter(user_id=request.session["user_id"])
        
        if request.method == "POST":
            
            if "logout" in request.POST:
                del request.session["user_id"]
                del request.session["username"]
                return HttpResponseRedirect("/vloggercafe/")
            
            elif "upload" in request.POST:
                fm = FileUpload(request.POST,request.FILES)
                if fm.is_valid():
                    user_id = request.session["user_id"]
                    video_title = fm.cleaned_data["video_title"]
                    video_hashtags = fm.cleaned_data["video_hashtags"]
                    video_desc = fm.cleaned_data["video_desc"]
                    video_filename = fm.cleaned_data["video_filename"]
                    video_thumbnail = fm.cleaned_data["video_thumbnail"]
                    published_date = date.today()
                    register = MasterVideoRecord(video_title=video_title,video_hashtags=video_hashtags,video_desc=video_desc,video_filename=video_filename,user_id=user_id,published_date=published_date,video_thumbnail=video_thumbnail)
                    register.save()

            elif "edit" in request.POST:
                fm2 = MyProfileSettings(request.POST, request.FILES)
                if fm2.is_valid():
                    user_id = request.session["user_id"]
                    myprofilepic = fm2.cleaned_data["myprofilepic"]
            
                    try:
                        profile_update = MyProfile.objects.get(user_id=user_id)
                    except MyProfile.DoesNotExist:
                        profile_update = None
                    
                    if profile_update:
                        profile_update.myprofilepic = myprofilepic
                    else:
                        profile_update = MyProfile(user_id=user_id, myprofilepic=myprofilepic)
                    
                    profile_update.save()
        
        fm = FileUpload()
        fm2 = MyProfileSettings()

    return render(request,"profile.html",{"location": loc,"form": fm,"session_info": session_info,"video_record": video_record,"fm2": fm2,"profile_settings": profile_settings})

def getSignUp(request):
    
    if "user_id" in request.session and "username" in request.session:
        return HttpResponseRedirect("/vloggercafe/")
    
    if request.method == "POST":
        fm = SignUp(request.POST)
        if fm.is_valid():
            user_id = uuid.uuid1()
            username = fm.cleaned_data["username"]
            email = fm.cleaned_data["email"]
            #hashing password
            password = fm.cleaned_data["password"]+"5gz"
            hashed_password = hashlib.md5(password.encode())
            register = UserSignUp(user_id=user_id,username=username,email=email,password=hashed_password.hexdigest())
            register.save()
            fm = SignUp()
    else:
        fm = SignUp() 
    return render(request,"signup.html",{"form": fm})

def getSignIn(request):
    
    if "user_id" in request.session and "username" in request.session:
            return HttpResponseRedirect("/vloggercafe/profile/")
    
    signin_error = False

    if request.method == "POST":
        fm = SignIn(request.POST)
        if fm.is_valid():
            username = fm.cleaned_data["username"]
            #hashing password
            password = fm.cleaned_data["password"]+"5gz"
            hashed_password = hashlib.md5(password.encode()).hexdigest()
            try:
                user_record = UserSignUp.objects.get(username=f"{username}",password=f"{hashed_password}")
                if user_record:
                    request.session["user_id"] = user_record.user_id
                    request.session["username"] = user_record.username
                    request.session.set_expiry(0)
                    return HttpResponseRedirect("/vloggercafe/profile/")
            except Exception:
                signin_error = True
            fm = SignIn()
    else:
        fm = SignIn() 
    return render(request,"signin.html",{"form": fm,"signin_error": signin_error})

def getClientIPAddress(request):
    client_ip,is_routable = get_client_ip(request)
    if client_ip is None:
        client_ip = "0.0.0.0"
        ip_type = "unknown"
    else:
        if is_routable:
            ip_type = "public"
        else:
            ip_type = "private"
    return client_ip,ip_type


def getClientLoc(request):
    ip_addr,_ = getClientIPAddress(request)
    res = requests.get(f"http://ip-api.com/json/{ip_addr}")
    location = json.loads(res.text)
    return location
