from django.contrib import admin
from .models import Student, Lecture, Check

admin.site.register(Student)
admin.site.register(Lecture)
admin.site.register(Check)
# Register your models here.
