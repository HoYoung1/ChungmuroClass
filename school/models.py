from datetime import datetime

from django.db import models
from django.utils import timezone


class Student(models.Model):
    student_id = models.CharField(max_length=64)
    name = models.CharField(max_length=12)
    img_url = models.CharField(max_length=64)
    reg_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Lecture(models.Model):
    professor = models.CharField(max_length=12)
    class_name = models.CharField(max_length=32)
    students = models.ManyToManyField(Student, null=True, blank=True)
    class_start = models.DateTimeField(default=timezone.now)
    regDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.class_name + '/' + self.professor

    # classtime이 현재시간-1시간 한 시각전이면 다 종료처리
    def state_lecture(self):
        if self.class_start < datetime.now() - datetime.timedelta(hours=1):
            return "end"
        else:
            return "on"


