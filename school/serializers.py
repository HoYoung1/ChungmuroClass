from school.models import Student, Lecture, Check
from rest_framework import serializers


class CheckSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Check
        fields = ('id', 'similarity', 'col_index')


class StudentSerializer(serializers.HyperlinkedModelSerializer):
    checks = serializers.StringRelatedField(many=True)

    class Meta:
        model = Student
        fields = ('id', 'student_id', 'name', 'img_url', 'checks')


class LectureSerializer(serializers.HyperlinkedModelSerializer):
    stateLecture = serializers.ReadOnlyField(source="state_lecture")

    class Meta:
        model = Lecture
        fields = ('id', 'professor', 'class_name', 'class_start', 'regDate', 'stateLecture')


class StudentJoinSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Student
        fields = ('id', 'student_id', 'name', 'img_url', 'reg_date')


class StudentNameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Student
        fields = ('id', 'name', 'img_url')


class LectureDetailSerializer(serializers.HyperlinkedModelSerializer):

    students = StudentNameSerializer(many=True, read_only=True)
    lecchecks = CheckSerializer(many=True, read_only=True)

    class Meta:
        model = Lecture
        fields = ('id', 'professor', 'class_name', 'class_start', 'students', 'lecchecks', 'regDate')
















