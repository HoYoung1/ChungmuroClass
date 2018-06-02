from PIL import Image, ImageDraw
import boto3
from pprint import pprint
from io import BytesIO
import imghelp
import cv2
import io

client = boto3.client('rekognition')
filename = 'test.jpg'
im = Image.open('test.jpg')
print(im.size)

def bbox_to_coords(bbox, img_width, img_height):
    '''Given a BoundingBox map (from Rekognition)
       return the corresponding coords
       suitable for use with ImageDraw rectangle.'''
    upper_left_x = bbox['Left'] * img_width
    upper_y = bbox['Top'] * img_height
    bottom_right_x = upper_left_x + (bbox['Width'] * img_width)
    bottom_y = upper_y + (bbox['Height'] * img_height)
    return [upper_left_x, upper_y, bottom_right_x, bottom_y]
imgbytes = imghelp.get_image_from_file(filename)

rekresp = client.detect_faces(Image={'Bytes': imgbytes},
                              Attributes=['ALL'])

# load the image in Pillow for processing
im = Image.open(BytesIO(imgbytes))

(img_width, img_height) = im.size

# prepare to draw on the image
draw = ImageDraw.Draw(im)

# pprint(rekresp)
for facedeets in rekresp['FaceDetails']:
    bbox = facedeets['BoundingBox']
    draw.rectangle(bbox_to_coords(bbox, img_width, img_height),
                   outline=(0,200,0))
del draw

i=0
save_path='C:/Users/User/Desktop/crop'
for facecut in rekresp['FaceDetails']:
    bbox = facecut['BoundingBox']
    crop_img = im.crop(bbox_to_coords(bbox, img_width, img_height))

    fname = "{}.jpg".format("{0:05d}".format(i))
    savename = save_path+fname
    crop_img.save(savename)
    i+=1
    #crop_img.show()
    #b= io.BytesIO()
    #crop_img.save(b, format="PNG")
    #img_bytes =b.getvalue()

#im.show()



#im.show()

