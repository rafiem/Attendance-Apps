from .models import User, Course
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model



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
  name    = serializers.CharField(max_length=100, required=True)
  code    = serializers.CharField(max_length=40, required=True, validators=[UniqueValidator(queryset=Course.objects.all())])
  dosen   = serializers.CharField(max_length=50, required=True)
  jurusan = serializers.CharField(max_length=40, required=True)

  def create(self, validated_data):
    course = Course.objects.create(**validated_data)
    return course