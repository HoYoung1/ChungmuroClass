#
#Created By 조성재
#
#매 1분마다 사진을 찍어 얼굴 좌표를 가지고 얼굴 부분만 하이라이트를 친 후 저장,
#하이라이트 친 사진을 어플리케이션과 통신이 가능하도록 AWS S3 Storage에 올림.
#
#


from datetime import datetime
from PIL import Image, ImageDraw
import cv2
import os
from boto3.s3.transfer import S3Transfer
import boto3
from pprint import pprint
from io import BytesIO
import requests


#bucket = 'chungmuroclass3'
bucket = 'chungmuroclass-userfiles-mobilehub-486279433'

class_num = x = input("Enter a number: ")

print(class_num)
video = cv2.VideoCapture(0)
first = datetime.now()
second = datetime.now()

print(video.isOpened())
def get_image_from_url(imgurl):  #성현이 추가코드
    resp = requests.get(imgurl)
    imgbytes = resp.content
    return imgbytes

def get_image_from_file(filename):
    with open(filename, 'rb') as imgfile:
        return imgfile.read()

def bbox_to_coords(bbox, img_width, img_height):  #json 에서 얼굴좌표 땡겨오는거 왼쪽위 오른쪽위 오른쪽아래 왼쪽아래, 사각형 꼭지점
    upper_left_x = bbox['Left'] * img_width
    upper_y = bbox['Top'] * img_height
    bottom_right_x = upper_left_x + (bbox['Width'] * img_width)
    bottom_y = upper_y + (bbox['Height'] * img_height)
    return [upper_left_x, upper_y, bottom_right_x, bottom_y]  #성현이 추가코드

picture_num = 1
while True:

    check, frame  = video.read()   #비디오를 읽어온다.

    cv2.imshow('image', frame)
    k = cv2.waitKey(1)

    if first.minute != second.minute:   #시간을 정해서 캡쳐를 할 수 있다.

        first = datetime.now()
        filename = first.year + first.month + first.day + first.hour + first.minute + first.second
        realfilename = str(filename) + '.jpg'
        cv2.imwrite(realfilename, frame)#만든 파일 이름으로1분마다 이미지 파일 저장
        #저장한 이미지 파일을 s3로 자동 업로드
        client = boto3.client('s3')
        transfer = S3Transfer(client)
        transfer.upload_file(os.getcwd() + '/' + realfilename, bucket, 'common' + '/' + realfilename)#realfile name 에 경로까지지정하면 s3내부에 경로가 생긴다.



        client = boto3.client('rekognition')  # boto3 '레코그니션' 사용 클라이언트  성현이 추가코드 여기서 레코그니션 클라이언트
        imgbytes = get_image_from_file(realfilename)  # 이미지헬프에서 파일이름이면 그냥 파일 열고 url 이면 연결해서 받아옴
        rekresp = client.detect_faces(Image={'Bytes': imgbytes},
                                      Attributes=['ALL'])  # json 애트리뷰트 얼굴 디텍트하는거인듯 레코그니션에서
        # load the image in Pillow for processing
        img = Image.open(BytesIO(imgbytes))

        (img_width, img_height) = img.size  # 인자값 두개가 너비 높이

        # prepare to draw on the image
        draw = ImageDraw.Draw(img)
        i = 0
        save_path = os.getcwd()  # 저장될 경로
        fname = str(class_num) + '_' + str(picture_num) + '.jpg'  # 파일 이름 및 형식
        #fname = "{}hilight.jpg".format("{0:05d}".format('hilight'))  # 파일 이름 및 형식
        #fname = "{}.jpg".format("{0:05d}".format(i))  # 파일 이름 및 형식
        # pprint(rekresp)
        savename = save_path + '/' +fname
        for facedeets in rekresp['FaceDetails']:  # 얼굴에 하이라이팅
            bbox = facedeets['BoundingBox']
            draw.rectangle(bbox_to_coords(bbox, img_width, img_height),
                           outline=(0, 200, 0))
        del draw

        img.save(savename)  # 지정경로에 지정이름으로 저장
        i += 1  # 파일 여러개 돌릴때 for문 더 넣어서 수정하면 댐
        picture_num += 1
        print(picture_num)
        img.show()  # 이미지 보이게     여기까지 성현이 코드 수정한 것

        client = boto3.client('s3')
        transfer = S3Transfer(client)
        transfer.upload_file(os.getcwd() + '/' + fname, bucket,
                             fname, extra_args={'ACL': 'public-read', 'ContentType': "image/jpeg"})  # file name 에 경로까지지정하면 s3내부에 경로가 생긴다.

    second = datetime.now()

    if k == ord('q'):
        break

picture_num = 1
video.release()
cv2.destroyAllWindows()
