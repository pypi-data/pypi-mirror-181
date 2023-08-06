from django.urls import path
from . import views


app_name = "login_app"
urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("login/loggin", views.login_auth, name="login_auth"),
    path("login/singing", views.signup_auth, name="signup_auth"),
    path("logout/", views.logout_view, name="logout"),
]
