from datetime import datetime, timedelta
from django.db import models
from django.utils import timezone
from school.tasks import say_hello, insert_check
import os


class Student(models.Model):
    student_id = models.CharField(max_length=64)
    name = models.CharField(max_length=12)
    img_url = models.CharField(max_length=64)
    reg_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


    def save(self, *args, **kwargs):
        print(self.name+" 학생이 등록되었습니다. ")
        super(Student, self).save(*args, **kwargs)
        dirname = str(self.id) + "_" + str(self.name)
        if not os.path.exists("userImg/"+dirname):
            os.mkdir("userImg/"+dirname)


class Lecture(models.Model):
    professor = models.CharField(max_length=12)
    class_name = models.CharField(max_length=32)
    students = models.ManyToManyField(Student, null=True, blank=True)
    class_start = models.DateTimeField(default=timezone.now)
    regDate = models.DateTimeField(auto_now_add=True)

    def __init__(self, *args, **kwargs):
        super(Lecture, self).__init__(*args, **kwargs)

    def __str__(self):
        return self.class_name + '/' + self.professor

    def save(self, *args, **kwargs):
        super(Lecture, self).save(*args, **kwargs)
        print("강의번호 : ", self.id)
        insert_check(self.id,schedule=self.class_start) #해당시간되면 작동하게??

        #To do
        #시간이 되면 반복문 돌면서 체크되게 하면될듯
        #스레드로 백그라운드로 시켜야합니다..1분간격으로 check db에 넣으면 되며
        #사진을 잘라서 이미지 잘려서 디렉토리에 들어가게 하면됩니다
        #def 로 백그라운드 하나 더 정의해야할듯





#현재시각이 5시이면 시작시간이 4시이전의 강의는 다 종료처리한다. 참가 가능수업과 종료수업 구별하기위해. 참가가능수업은 한개만가능함
    def state_lecture(self):
        if self.class_start < datetime.now() - timedelta(hours=1):
            return "end"
        else:
            return "on"


class Check(models.Model):
    user_id = models.ForeignKey(Student, related_name='checks')
    lecture_id = models.ForeignKey(Lecture, related_name='lecchecks', on_delete=models.CASCADE)
    similarity = models.IntegerField()
    col_index = models.IntegerField()
    regDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.lecture_id.__str__() + '/' + self.user_id.__str__() + ' / 인덱스 : ' + str(self.col_index)

    def __unicode__(self):
        return '%d: %d' % (self.similarity, self.col_index)
