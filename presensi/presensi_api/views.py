from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from .serializers import UserSerializer, CourseSerializer, CourseTokenSerializer
from .models import User, Course
from rest_framework.decorators import parser_classes
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)


class Login(APIView):
  permission_classes = ()

  def post(self, request):
    email = request.data.get("email")
    password = request.data.get("password")
    if email is None or password is None:
      return Response({'error': 'Please provide both email and password'}, status=HTTP_400_BAD_REQUEST)

    try:
      user = User.objects.get(email=email)
    except User.DoesNotExist:
      user = None
    
    if not user:
      return Response({'error': 'Invalid Email'}, status=HTTP_404_NOT_FOUND)
    else:
      if not user.check_password(password):
        return Response({'error': 'Invalid Password'}, status=HTTP_404_NOT_FOUND)

    token, _ = Token.objects.get_or_create(user=user)
    return Response({'Authentication Token': token.key}, status=HTTP_200_OK)


class Logout(APIView):
  def get(self, request):
      request.user.auth_token.delete()
      return Response({'success': 'Success Logout'}, status=HTTP_200_OK)


class Register(APIView):
  permission_classes  = ()

  def post(self, request):
    user_serializer = UserSerializer(data=request.data)
    if user_serializer.is_valid():
      user_serializer.save()
      return Response({'success': 'Success register new user'}, status=HTTP_200_OK)
    else:
      return Response(user_serializer.errors, status=HTTP_400_BAD_REQUEST)
    return Response(user_serializer.errors, status=HTTP_400_BAD_REQUEST)


class ProfileUser(APIView):

  def get(self, request):
    user_profile = User.objects.get(pk=request.user.id)
    serializer = UserSerializer(user_profile)
    return Response(serializer.data)


class CourseMain(APIView):
  permission_classes = (IsAdminUser,)

  def get(self, request):
    courses = Course.objects.filter()
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)

  def post(self, request):
    course_serializer = CourseSerializer(data=request.data)
    if course_serializer.is_valid():
      course_serializer.save()
      return Response({'success': 'Success create new course'}, status=HTTP_200_OK)
    else:
      return Response(course_serializer.errors, status=HTTP_400_BAD_REQUEST)
    return Response(course_serializer.errors, status=HTTP_400_BAD_REQUEST)


class CourseToken(APIView):
  permission_classes = (IsAdminUser,)

  def get(self, request, id):
    try:
      course = Course.objects.get(pk=id)
    except Course.DoesNotExist:
      course = None
    
    if not course:
      return Response({'error': 'Invalid Course ID'}, status=HTTP_404_NOT_FOUND)
    else:
      serializer = CourseTokenSerializer(course)
      return Response(serializer.data)
