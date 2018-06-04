#
#Created By 김성현
#이미지 가져오기 모듈
#
#


import requests

def get_image_from_url(imgurl):
    resp = requests.get(imgurl)
    imgbytes = resp.content
    return imgbytes


def get_image_from_file(filename):
    with open(filename, 'rb') as imgfile:
        return imgfile.read()
