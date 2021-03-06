from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from .serializers import UserSerializer, CourseSerializer, CourseTokenSerializer, AttendClassSerializer, CourseAttendHistory
from .models import User, Course, Attendance
from rest_framework.decorators import parser_classes
from rest_framework.response import Response
from .utils import get_object_by_field, get_response_by_object, get_response_serializer_valid
from datetime import date, datetime, time
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

    user = get_object_by_field(User, email, "email")

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
    response = get_response_serializer_valid(user_serializer, success_msg="Success Registering New User")
    
    return response


class ProfileUser(APIView):

  def get(self, request):
    user_profile = User.objects.get(pk=request.user.id)
    serializer = UserSerializer(user_profile)

    return Response(serializer.data)


class CourseMain(APIView):
  # Only available for admin
  permission_classes = (IsAdminUser,)

  # Get all list of course
  def get(self, request):
    courses = Course.objects.all()
    serializer = CourseSerializer(courses, many=True)

    return Response(serializer.data)

  # Create new course
  def post(self, request):
    course_serializer = CourseSerializer(data=request.data, partial=True)
    response = get_response_serializer_valid(course_serializer, success_msg="Success Creating New Course")
    
    return response


class CourseUnit(APIView):

  def get(self, request, id):
    course    = get_object_by_field(Course, id, "pk")
    response  = get_response_by_object(CourseSerializer, course, error_msg="Course not exist or invalid course id")

    return response


class CourseToken(APIView):
  permission_classes = (IsAdminUser,)

  def get(self, request, id):
    course    = get_object_by_field(Course, id, "pk")
    response  = get_response_by_object(CourseTokenSerializer, course, error_msg="Course not exist or invalid course id")

    return response


class ApplyCourse(APIView):
  permission_classes = (IsAdminUser,)

  def post(self, request, id):
    if "user_id" not in request.data:
      return Response({"error": "Parameter 'user_id' is required"})

    course    = get_object_by_field(Course, id, "pk")
    user      = get_object_by_field(User, request.data["user_id"], "pk")
    course.user.add(user)
    
    return Response({'success': 'Success adding user to the course'})


class AttendClass(APIView):

  def post(self, request):
    if "token" not in request.data:
      return Response({"error": "Parameter 'token' is required"})

    course = get_object_by_field(Course, request.data["token"], "token")
    if not course:
      return Response({"error": "No course is match for this token"})

    member_of_course = Course.objects.filter(user__id=request.user.id, id=course.id)
    if not member_of_course:
      return Response({"error": "You are not a part of this course"})

    data = {"user_id": request.user.id, "course_id": course.id}
    serializer = AttendClassSerializer(data=data, partial=True)
    response = get_response_serializer_valid(serializer, "Success attend a course this week")

    return response


class UserCourse(APIView):

  def get(self, request):
    courses = Course.objects.filter(user__id=request.user.id)
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)


class UserAttend(APIView):

  def get(self, request, id):
    course    = get_object_by_field(Course, id, "pk")
    if not course:
      return Response({"error": "Course not exist or invalid course id"})

    member_of_course  = Attendance.objects.filter(user_id=request.user.id, course_id=course.id)
    serializer        = AttendClassSerializer(member_of_course, many=True)

    return Response(serializer.data)


class CourseHistoryAttend(APIView):

  def get(self, request, id):
    course    = get_object_by_field(Course, id, "pk")
    if not course:
      return Response({"error": "Course not exist or invalid course id"})

    attend_history = Attendance.objects.filter(course_id=course.id).values("time_present__date").distinct()
    serializer = CourseAttendHistory(attend_history, many=True)

    return Response(serializer.data)


    

