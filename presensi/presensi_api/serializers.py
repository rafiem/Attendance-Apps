from .models import User, Course, Attendance
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from rest_framework.validators import UniqueValidator
from django.utils import timezone
from datetime import date, datetime, time
from uuid import uuid4



class UserSerializer(serializers.Serializer):
  name = serializers.CharField(required=True, max_length=50)
  email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
  password = serializers.CharField(write_only=True, required=True, min_length=6)
  nim = serializers.CharField(required=True, max_length=20, validators=[UniqueValidator(queryset=User.objects.all())])
  jurusan = serializers.CharField(required=True, max_length=50)
  fakultas = serializers.CharField(required=True, max_length=50)


  def create(self, validated_data):
    validated_data['password'] = make_password(validated_data.get('password'))
    user = User.objects.create(**validated_data)
    return user

  def update(self, instance, validated_data):
    instance.name     = validated_data.get('name', instance.name)
    instance.save()
    return instance


class CourseSerializer(serializers.Serializer):
  id      = serializers.IntegerField()
  name    = serializers.CharField(max_length=100, required=True)
  code    = serializers.CharField(max_length=40, required=True, validators=[UniqueValidator(queryset=Course.objects.all())])
  dosen   = serializers.CharField(max_length=50, required=True)
  jurusan = serializers.CharField(max_length=40, required=True)
  start_time = serializers.DateTimeField(required=True)
  end_time   = serializers.DateTimeField(required=True)

  def validate(self, data):
    if data["end_time"] < data["start_time"]:
      raise serializers.ValidationError({
          "error": "Start time cannot be greater than end time",
      })

    return super(CourseSerializer, self).validate(data)

  def create(self, validated_data):
    validated_data['token'] = uuid4().hex
    course = Course.objects.create(**validated_data)
    return course

class CourseTokenSerializer(serializers.Serializer):
  token   = serializers.CharField()


class AttendClassSerializer(serializers.Serializer):
  user_id     = serializers.IntegerField()
  course_id   = serializers.IntegerField()

  def create(self, validated_data):
    validated_data["time_present"] = datetime.now()
    day_submit  = validated_data["time_present"].strftime('%a')
    time_submit = validated_data["time_present"].time()
    
    course      = Course.objects.get(pk=validated_data["course_id"])

    day_course  = course.start_time.strftime("%a")
    start_time  = course.start_time.time()
    end_time    = course.end_time.time()

    if day_submit == day_course:
      if time_submit >= start_time and time_submit <= end_time:
        attend_course = Attendance.objects.create(**validated_data)
        return attend_course
    
    raise serializers.ValidationError({
      "error": "Not in time for that course schedule",
    })

