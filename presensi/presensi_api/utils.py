from .models import User, Course
from .serializers import UserSerializer, CourseSerializer, CourseTokenSerializer
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)


def get_object_by_field(model_, var_input, var_field):
  try:
    dictionary = {var_field: var_input}
    obj = model_.objects.get(**dictionary)
  except:
    obj = None

  return obj


def get_response_by_object(serializer_, obj, error_msg):
  if not obj:
    return Response({'error': error_msg}, status=HTTP_404_NOT_FOUND)
  else:
    serializer = serializer_(obj)
    return Response(serializer.data)


def get_response_serializer_valid(serializer_, success_msg):
  if serializer_.is_valid():
    serializer_.save()
    return Response({'success': success_msg}, status=HTTP_200_OK)
  else:
    return Response(serializer_.errors, status=HTTP_400_BAD_REQUEST)