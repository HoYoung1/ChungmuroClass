from PIL import Image, ImageDraw
import boto3
from pprint import pprint
from io import BytesIO
import imghelp

def bbox_to_coords(bbox, img_width, img_height):
    '''Given a BoundingBox map (from Rekognition)
       return the corresponding coords
       suitable for use with ImageDraw rectangle.'''
    upper_left_x = bbox['Left'] * img_width
    upper_y = bbox['Top'] * img_height
    bottom_right_x = upper_left_x + (bbox['Width'] * img_width)
    bottom_y = upper_y + (bbox['Height'] * img_height)
    return [upper_left_x, upper_y, bottom_right_x, bottom_y]

client = boto3.client('rekognition')

filenames = 'test.jpg'
#imgbytes = imghelp.get_image_from_url(imgurl)
imgbytes = imghelp.get_image_from_file(filenames)

rekresp = client.detect_faces(Image={'Bytes': imgbytes},
                              Attributes=['ALL'])

# load the image in Pillow for processing
img = Image.open(BytesIO(imgbytes))

(img_width, img_height) = img.size

# prepare to draw on the image
draw = ImageDraw.Draw(img)

# pprint(rekresp)
for facedeets in rekresp['FaceDetails']:
    bbox = facedeets['BoundingBox']
    draw.rectangle(bbox_to_coords(bbox, img_width, img_height),
                   outline=(0,200,0))
del draw

img.show()
