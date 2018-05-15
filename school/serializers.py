from school.models import Student, Lecture
from rest_framework import serializers


class StudentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Student
        fields = ('id', 'student_id', 'name', 'img_url', 'reg_date')


class LectureSerializer(serializers.HyperlinkedModelSerializer):
    stateLecture = serializers.ReadOnlyField(source="state_lecture")
    class Meta:
        model = Lecture
        fields = ('id', 'professor', 'class_name', 'class_start', 'regDate','stateLecture')


class StudentJoinSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Student
        fields = ('id', 'student_id', 'name', 'img_url', 'reg_date')


class LectureDetailSerializer(serializers.HyperlinkedModelSerializer):

    students = StudentSerializer(many=True, read_only=True)

    class Meta:
        model = Lecture
        fields = ('id', 'professor', 'class_name', 'students', 'class_start', 'regDate')
















