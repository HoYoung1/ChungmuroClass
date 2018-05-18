"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from rest_framework import routers
from school import views as school_views

router = routers.DefaultRouter()
router.register(r'school/students', school_views.StudentViewSet)
router.register(r'school/lectures', school_views.LectureViewSet)
router.register(r'school/checks', school_views.CheckViewSet)

urlpatterns = [
    url(r'^school/students/join/', school_views.student_join),
    url(r'^school/students/changeimg/', school_views.student_changeimg),
    # img 바꿀수있게.
    url(r'^school/lectures/istaken/', school_views.student_istaken),
    url(r'^school/lectures/take/', school_views.student_takeclass),
    url(r'^school/lectures/(?P<pk>\d+)/$', school_views.lecture_detail),
    # lectures/1, lectures/2 이런식으로 request 올꺼임.
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', admin.site.urls),

    # ^ : 문자열이 시작할 때
    # $ : 문자열이 끝날 때
    # \d: 숫자
    # . : 바로 앞에 나오는 항목이 계속 나올 때
    # (): 패턴의 부분을 저장할때
]
