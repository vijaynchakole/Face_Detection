import os
from app import app
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

from flask import Flask, request, jsonify
import urllib.request
from face_processing import FaceProcessing


import cv2
import numpy as np
import requests


fc = FaceProcessing()

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
@app.route('/')
def upload_form():
	return render_template('upload.html')


@app.route('/', methods=['POST'])
def upload_image():
    file = request.files['file']
    filename=file.filename
    # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    file.save((app.config['UPLOAD_FOLDER'] + "/" + filename))
    # IMAGE_PATH = (os.path.join(app.config['UPLOAD_FOLDER'], filename))
    IMAGE_PATH = (app.config['UPLOAD_FOLDER'] + "/" + filename)
    # resize image
    image = cv2.imread(IMAGE_PATH, cv2.IMREAD_UNCHANGED)
    
    WIDTH = 640
    HEIGHT = 640
    DIM = (WIDTH, HEIGHT)
    
    image = cv2.resize(image,DIM, interpolation = cv2.INTER_AREA)
    
    status = cv2.imwrite(IMAGE_PATH, image)
    
    # IMAGE_PATH = "C:\\Users\\hp\\Desktop\\practicals_ml\\OpenCV\\Projects\\Project-07\\static\\uploads\\test_image_4.jpg"
    image=open(IMAGE_PATH,"rb")
    result = fc.face_detection(image.read())
    #image_array = np.asarray(bytearray(image.read()),dtype=np.uint8)
    #img_opencv = cv2.imdecode(image_array, -1)
    img_opencv = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    for face in result:
        left, top, right, bottom = face['box']
        print(left, top, right, bottom)
        # To draw a rectangle, you need top-left corner and bottom-right corner of rectangle:
        cv2.rectangle(img_opencv, (left,top), (right,bottom), (0, 255, 255), 2)
        # Draw top-left corner and bottom-right corner (checking):
        cv2.circle(img_opencv, (left, top), 5, (0, 0, 255), -1)
        cv2.circle(img_opencv, (right, bottom), 5, (255, 0, 0), -1)
    #img_opencv.save(os.path.join(app.config['UPLOAD_FOLDER'],("detect.jpg"))) 
    # current_dir = os.getcwd()
    # img_path = "C:\\Users\\hp\\Desktop\\practicals_ml\\OpenCV\\Projects\\Project-07\\static\\uploads\\output_image.jpg"
    
    seperate = filename.split(".")
    img_path = "static/uploads/output_" + seperate[0] + "." + seperate[1]
    status = cv2.imwrite(img_path, img_opencv)
    print(status)
    output = "output_" + seperate[0] + "." + seperate[1]
    return render_template('upload.html', filename=[filename,output])



@app.route('/display/<filename>')
def display_image(filename):
	#print('display_image filename: ' + filename)
	return redirect(url_for('static', filename='uploads/' + filename), code=301)

if __name__ == "__main__":
    app.run()
