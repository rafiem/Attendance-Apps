from django.contrib import admin
from django.urls import path
from .views import (
  Login,
  Logout,
  Register,
  ProfileUser,
  UserCourse,
  CourseMain,
  CourseUnit,
  CourseHistoryAttend,
  CourseToken,
  ApplyCourse,
  AttendClass,
  UserAttend
)


urlpatterns = [
  path('login/', Login.as_view(), name='login'),
  path('logout/', Logout.as_view(), name='logout'),
  path('register/', Register.as_view(), name='register'),
  path('user/profile/', ProfileUser.as_view(), name='user_profile'),
  path('user/course/', UserCourse.as_view(), name='user_course'),
  path('user/course/<str:id>/attendance/', UserAttend.as_view(), name='user_attend'),
  path('course/', CourseMain.as_view(), name='course_main'),
  path('course/<str:id>/', CourseUnit.as_view(), name='course_unit'),
  path('course/<str:id>/token/', CourseToken.as_view(), name='course_token'),
  path('course/<str:id>/apply/', ApplyCourse.as_view(), name='course_apply'),
  path('course/<str:id>/attend_history/', CourseHistoryAttend.as_view(), name='course_attend_history'),
  path('attend_class/', AttendClass.as_view(), name='attend_class')
]