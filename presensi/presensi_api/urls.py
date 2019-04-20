from django.contrib import admin
from django.urls import path
from .views import (
  Login,
  Logout,
  Register,
  ProfileUser,
  CourseMain
)


urlpatterns = [
  path('login/', Login.as_view(), name='login'),
  path('logout/', Logout.as_view(), name='logout'),
  path('register/', Register.as_view(), name='register'),
  path('profile/', ProfileUser.as_view(), name='profile'),
  path('course/', CourseMain.as_view(), name='course_main')
]