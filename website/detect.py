from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, Response
from werkzeug.utils import secure_filename
import cv2
import os
import numpy as np
from keras.models import load_model
from skimage.transform import resize, pyramid_reduce
import PIL
from PIL import Image

detect = Blueprint('detect', __name__)

model = load_model('CNNmodel.h5')

camera=cv2.VideoCapture(0)

def prediction(pred):
    return(chr(pred+ 65))


def keras_predict(model, image):
    data = np.asarray( image, dtype="int32" )
    
    pred_probab = model.predict(data)[0]
    pred_class = list(pred_probab).index(max(pred_probab))
    return max(pred_probab), pred_class

def keras_process_image(img):
    
    image_x = 28
    image_y = 28
    img = cv2.resize(img, (1,28,28), interpolation = cv2.INTER_AREA)
  
    return img

def crop_image(image, x, y, width, height):
    return image[y:y + height, x:x + width]

def generate_frames():
    while True:
            
        ## read the camera frame
        success,image_frame=camera.read()
        if not success:
            print("not");
            break
        else:
            im2 = crop_image(image_frame, 300,300,300,300)
            image_grayscale = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)
    
            image_grayscale_blurred = cv2.GaussianBlur(image_grayscale, (15,15), 0)
            im3 = cv2.resize(image_grayscale_blurred, (28,28), interpolation = cv2.INTER_AREA)

            im4 = np.resize(im3, (28, 28, 1))
            im5 = np.expand_dims(im4, axis=0)

            pred_probab, pred_class = keras_predict(model, im5)
        
            curr = prediction(pred_class)
            print(curr)
            # text_out += curr

            cv2.putText(image_frame, curr, (700, 300), cv2.FONT_HERSHEY_COMPLEX, 4.0, (255, 255, 255), lineType=cv2.LINE_AA)


            cv2.rectangle(image_frame, (300, 300), (600, 600), (255, 255, 00), 3)
            ret,buffer=cv2.imencode('.jpg',image_frame)
            image_frame=buffer.tobytes()

        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + image_frame + b'\r\n')

@detect.route('/detect', methods=['GET', 'POST'])
def detects():
    return render_template("detect.html")

@detect.route('/video')
def video():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')
