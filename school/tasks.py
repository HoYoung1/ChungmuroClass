#
#Created By 김성현,김호영
#
#포그라운드에서 돌릴경우 60분동안 응답이 안됨, 백그라운드 환경에서 체크가 되어야 하므로 백그라운드환경에서 돌림
#
#d

from __future__ import absolute_import
from PIL import Image, ImageDraw, ImageFont
import boto3
from pprint import pprint
from io import BytesIO
from datetime import datetime
import requests
import time
from boto3.s3.transfer import S3Transfer

from background_task import background

from mysite.celery import app

# @app.task
from school import models


# Created By 김호영
@background(schedule=1)
def say_hello():  # 실제 백그라운드에서 작업할 내용을 task로 정의한다.
    print("Hello, celery!")

# Created By 김호영
@background(schedule=60)
def test_bg(id):
    print("되라제발좀")
    l1 = models.Lecture.objects.get(id=id)
    l1.professor = '호영으로바뀌나..?'
    l1.save()

# Created By 김호영
@background(schedule=60)  # 디폴트값은 60이나 시작하는시간을 인자로 전달해줌
def insert_check(id):
    print("강의번호 : ", id)
    print("체크가 시작됩니다.")
    CGREENBG = '\33[42m'
    CGREEN = '\33[44m'
    CRED = '\033[91m'
    CEND = '\33[0m'
    waitFlag = False  # 이거 플래그 안세워놓으니까 aws api 리턴값 받아올때 다른짓 하려고한다.. 리턴값받아와야 다음을 할수있게 !
    first = datetime.now()
    keysecond = first.second
    for i in range(60):  # 60번 반복이다 수업시간은 60분임.
        if i != 0:
            while True:
                second = datetime.now()
                if second.second == keysecond:
                    print("연산 시작")
                    break
                elif (second.second + 5)%60 == keysecond:
                    print(CRED + "연산 시작 5초전" + CEND)
                    print(CRED + "연산 시작 5초전" + CEND)
                    print(CRED + "연산 시작 5초전" + CEND)
                    print(CRED + "연산 시작 5초전" + CEND)
                    break
        lec = models.Lecture.objects.get(id=id)
        for stu in lec.students.all():
            print()
            print()
            print()

            print( "******** " + CGREEN + stu.name + CEND  + " 학생의 FaceMatch 를 시작합니다" + "******** ")
            dirname = "userImg/" + str(stu.id) + "_" + str(
                stu.name)  # 잘라진 이미지가 어디 저장될지도 인자로 전달해줘야함. 이 디렉토리는 유저가 새로 추가될때 자동으로 생성됨.
            targetName = str(id) + "_" + str(i+1)+".jpg"
            similar = faceS(targetName, stu.img_url,
                            dirname, stu.name)  # 이부분이 핵심임 aws api 사용해서 유사도 값도받아오고 얼굴 이미지도잘라서 디렉토리에 넣음 .

            chk = models.Check(user_id=stu, lecture_id=lec, similarity=int(similar), col_index=i)
            chk.save()
        print("현재 : " + str(i) + "분 / 60 분")
        print("다음 60초를 기다립니다.")
        time.sleep(1)  

# Created By 조성재
@background(schedule=60)
def LearningModelStart():
    test = 0
    # for test
    # for test 2
    

# Created By 김성현
def get_image_from_url(imgurl):
    resp = requests.get(imgurl)
    imgbytes = resp.content
    return imgbytes

# Created By 김성현
def get_image_from_file(filename):
    with open(filename, 'rb') as imgfile:
        return imgfile.read()

# Created By 김성현
def bbox_to_coords(bbox, img_width, img_height):  # json 에서 얼굴좌표 땡겨오는거 왼쪽위 오른쪽위 오른쪽아래 왼쪽아래, 사각형 꼭지점
    upper_left_x = bbox['Left'] * img_width
    upper_y = bbox['Top'] * img_height
    bottom_right_x = upper_left_x + (bbox['Width'] * img_width)
    bottom_y = upper_y + (bbox['Height'] * img_height)
    return [upper_left_x, upper_y, bottom_right_x, bottom_y]


# Created By 김성현
def bbox_to_coords_with_z(bbox, img_width, img_height,z):  # json 에서 얼굴좌표 땡겨오는거 왼쪽위 오른쪽위 오른쪽아래 왼쪽아래, 사각형 꼭지점
    upper_left_x = bbox['Left'] * img_width
    upper_y = bbox['Top'] * img_height
    bottom_right_x = upper_left_x + (bbox['Width'] * img_width)
    bottom_y = upper_y + (bbox['Height'] * img_height)
    return [upper_left_x+z, upper_y+z, bottom_right_x+z, bottom_y+z]

# Created By 김성현
def faceS(target, source, dirname,stuName):
    CGREENBG = '\33[42m'
    CGREEN = '\33[44m'
    CEND = '\33[0m'
    print("target(수업중찍힌사진) : ", target)
    print("source(학생프로필사진) : ", source)

    bucket = 'chungmuroclass-userfiles-mobilehub-486279433'
    sourceFile = source
    targetFile = target

    client = boto3.client('rekognition')
    s3 = boto3.client('s3')

    try:
        response = client.compare_faces(SimilarityThreshold=55,
                                        SourceImage={'S3Object': {'Bucket': bucket, 'Name': sourceFile}},
                                        TargetImage={'S3Object': {'Bucket': bucket, 'Name': targetFile}})
    except Exception as e:
        print()
        print("compare_faces API 호출 중 에러가 발생하였습니다.")
        print()
        return 101

    #print(response) #response는 일단 출력하지말자 값이너무많음.


    url = '{}/{}/{}'.format(s3.meta.endpoint_url, bucket, target)
    imgbytes = get_image_from_url(url)


    img = Image.open(BytesIO(imgbytes))  # 이거 사용하려면 버킷 폴리시 설정 변경해야함
    (img_width, img_height) = img.size
    draw = ImageDraw.Draw(img)

    save_path = dirname
    # fname = "{}.jpg".format("{0:05d}".format(2))
    fname = datetime.today().strftime("%Y%m%d%H%M%S") + ".jpg"
    savename = save_path + "/" + fname
    maxSimilar = 0
    for faceMatch in response['FaceMatches']:
        similar = faceMatch['Similarity']
        if similar > maxSimilar:
            maxSimilar = similar
        print()
        print()
        position = faceMatch['Face']['BoundingBox']
        confidence = str(faceMatch['Face']['Confidence'])
        print()

        # draw.rectangle(bbox_to_coords(position, img_width, img_height)
        #

        print(CGREEN + "일치율 : " + str(similar) + CEND)


        if similar > 80:  # 80이상일때만자르자
            crop_img = img.crop(bbox_to_coords(position, img_width, img_height))
            crop_img.save(savename)
            print("#######"+" 얼굴이 정상적으로 crop되어 해당 유저 디렉토리에 저장되었습니다."+" #######")
            print("Crop 된 이미지 저장 경로 :./" + savename)

            xy = bbox_to_coords_with_z(position, img_width, img_height, 1)

            #font = ImageFont.truetype("arial.ttf", 20)

            font = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSerif.ttf", 20)


            draw.text((xy[0], xy[3]), str(similar)+"%"+stuName,font=font, fill="red")

            img.save("./edit.jpg")

            client = boto3.client('s3')
            transfer = S3Transfer(client)
            transfer.upload_file("./edit.jpg", bucket,
                                 targetFile, extra_args={'ACL': 'public-read',
                                                    'ContentType': "image/jpeg"})  # file name 에 경로까지지정하면 s3내부


    return maxSimilar
