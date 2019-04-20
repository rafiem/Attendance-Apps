from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
  name      = models.CharField(max_length=40)
  email     = models.EmailField(max_length=64)
  password  = models.CharField(max_length=100)
  nim       = models.CharField(max_length=20)
  jurusan   = models.CharField(max_length=50)
  fakultas  = models.CharField(max_length=50)
  is_admin  = models.BooleanField(default=False)


  def __str__(self):
    return self.name


class Course(models.Model):
  name        = models.CharField(max_length=100)
  token       = models.CharField(max_length=100)
  code        = models.CharField(max_length=40)
  dosen       = models.CharField(max_length=50)
  jurusan     = models.CharField(max_length=40)
  start_time  = models.DateTimeField()
  end_time    = models.DateTimeField()
  user        = models.ManyToManyField(User)

  def __str__(self):
    return self.name


class Attendance(models.Model):
  user          = models.ForeignKey(User, on_delete=models.CASCADE)
  course        = models.ForeignKey(Course, on_delete=models.CASCADE)
  time_present  = models.DateTimeField()

  def save(self, *args, **kwargs):
    self.time_present = timezone.now()
    
    return super(User, self).save(*args, **kwargs)



