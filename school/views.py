from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.utils import json

from school.serializers \
    import StudentSerializer, LectureSerializer, StudentJoinSerializer, LectureDetailSerializer, CheckSerializer
from school.models import Student, Lecture, Check
from django.http import HttpResponse, JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class LectureViewSet(viewsets.ModelViewSet):

    queryset = Lecture.objects.all().order_by("-id")
    serializer_class = LectureSerializer


class CheckViewSet(viewsets.ModelViewSet):
    queryset = Check.objects.all()
    serializer_class = CheckSerializer


@csrf_exempt # csrf라는 어떤 인증절차같은게 있는데 예외처리를 해준다. 안하면 에러뜸
def student_join(request):
    # 회원가입 아님, 로그인 이라고 봐야함. 결과값을 보고 회원가입된유저인지 아닌지 판단함.
    print('join start')
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    student_id = body['student_id']
    #print(student_id)
    #print(name)
    #print(img_url)

    try:
        #기존 id(token)가 있다면 모든정보를 넘겨준다. 없다면 0을 리턴함.
        student = Student.objects.get(student_id=student_id) #토큰으로 찾아야함
        serializer = StudentJoinSerializer(student, context={'request'})
        return JsonResponse(serializer.data)
    except Student.DoesNotExist:
        return JsonResponse(
            {
                'student_id': "0"
            }
        )

    # if(request.method == 'GET'):
    #     serializer = StudentJoinSerializer(student, context={'request'})
    #     return JsonResponse(serializer.data)



@csrf_exempt
def student_istaken(request):

    # 수업참가버튼을 누를때 이미 참가버튼을 눌렀었던 학생은 True를 반환합니다
    print('istaken start')
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    # 어떤학생으로 부터의 응답인지, 어떤 강의를 참가하고싶은지 키값을 받습니다.
    student_id = body['student_id']
    lecture_id = body['lecture_id']

    lec = Lecture.objects.get(id=lecture_id)
    print(lec)
    try:
        # 수업에 참여한 학생이라고 기록되어있는경우,
        if lec.students.get(student_id=student_id):
            print("로그확인중입니다.")
            print(lec.students.get(student_id=student_id))
            return JsonResponse(
                {
                    'isExist': True,
                    'msg': 'already exist'
                }
            )
    except Student.DoesNotExist:
        # 수업에 참여하지 않은 학생 , False를 반환.
        return JsonResponse(
            {
                'isExist': False,
                'msg': 'need participate in'
            }
        )


@csrf_exempt
def student_takeclass(request):
    # 수업에 참가하는 메소드
    print('takeclass start')
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    # 어떤학생으로 부터의 응답인지, 어떤 강의를 참가하고싶은지 키값을 받습니다.
    student_id = body['student_id']
    lecture_id = body['lecture_id']


    try:
        stu = Student.objects.get(student_id=student_id)
        lec = Lecture.objects.get(id=lecture_id)
        print(stu)
        print(lec)

        # 수업에 참가합니다
        lec.students.add(stu)
        return JsonResponse(
            {
                'isExist': True,
                'msg': 'take class Success'
            }
        )

    except Student.DoesNotExist:
        return JsonResponse(
            {
                'isExist': False,
                'msg': 'student exist error'
            }
        )

    except Lecture.DoesNotExist:
        return JsonResponse(
            {
                'isExist': False,
                'msg': 'lecture exist error'
            }
        )


@csrf_exempt
def lecture_detail(request, pk):
    # 해당 수업을 듣는 학생들을 반환합니다.

    print('lecture_detail start')
    try:
        lecture = Lecture.objects.get(pk=pk)
    except Lecture.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = LectureDetailSerializer(lecture, context={'request': request})
        return JsonResponse(serializer.data)


@csrf_exempt
def student_changeimg(request):
    # 사용자는 이미지 url을 바꿀수있음.

    print('student changeurl start')
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    # student_id 와 img_url을 받아서 update합니다.
    student_id = body['student_id']
    img_url = body['img_url']

    try:
        stu = Student.objects.get(student_id=student_id)
        stu.img_url = img_url
        stu.save()
        return JsonResponse(
            {
                'isExist': True,
                'msg': 'student img_url is changed'
            }
        )

    except Student.DoesNotExist:
        return JsonResponse(
            {
                'isExist': False,
                'msg': 'student exist error'
            }
        )

@csrf_exempt
def download_apk(request):
    #response = FileResponse(open('1.jpg', 'rb'), content_type='image/png')
    response = FileResponse(open('apk/attendance_check.apk', 'rb'), content_type='application/apk')
    return response





    # body_unicode = request.body.decode('utf-8')
    # body = json.loads(body_unicode)
    #
    # lecture_id = body['lecture_id']
    #
    # try:
    #     lec = Lecture.objects.get(id=lecture_id)
    #     print(lec.students.all())
    #
    #     taken_students = lec.students.all()
    #     serializer = TakenStudentSerializer(taken_students, context={'request'})
    #     return JsonResponse(
    #         {
    #             'isValid': True,
    #             'students': serializer.data
    #         }
    #     )
    #
    # except Student.DoesNotExist:
    #     return JsonResponse(
    #         {
    #             'isValid': False,
    #             'msg': 'student not exist '
    #         }
    #     )
    #
    # except Lecture.DoesNotExist:
    #     return JsonResponse(
    #         {
    #             'isValid': False,
    #             'msg': 'lecture not exist '
    #         }
    #     )


