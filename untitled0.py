# -*- coding: utf-8 -*-
"""
Created on Tue May 12 13:00:11 2020

@author: hp
"""

line = "vijay is bad"
line = "vijay_test_image.jpg"

new =line.split(".")
new
type(new)
new[0]
new[1]

import requests

url = 'https://www.w3schools.com/python/demopage.php'

path = "C:/Users/hp/Desktop/All_Images/test_images/student_05.jpg"
myfiles = {'file': open(path ,'rb')}

x = requests.post(url, files = myfiles)

#print the response text (the content of the requested file):

print(x.text)
