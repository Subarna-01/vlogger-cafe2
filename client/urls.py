from django.urls import path
from client import views

urlpatterns = [
    path("",views.getIndex),
    path("profile/",views.getProfile),
    path("signup/",views.getSignUp),
    path("signin/",views.getSignIn),
]