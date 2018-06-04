#
#Created By 정욱
#
#관리자 페이지에서 사용할 요소들 기입
#
#

from django.contrib import admin
from .models import Student, Lecture, Check

admin.site.register(Student)
admin.site.register(Lecture)
admin.site.register(Check)
# Register your models here.
