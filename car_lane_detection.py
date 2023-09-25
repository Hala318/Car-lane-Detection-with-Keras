# -*- coding: utf-8 -*-
"""Car Lane detection.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ANYc3t0JVOYLtlO7fVcQZ4sBPkAR4R2C
"""

from google.colab import files

uploaded= files.upload()

!pip install scipy==1.1.0

import numpy as np
import cv2
from skimage.transform import resize
from moviepy.editor import VideoFileClip
from tensorflow import keras

model = keras.models.load_model('model.h5')

class Lanes():
  def __init__(self):
    self.recent_fit=[]
    self.avg_fit =[]

def road_lines(image):
    small_img=resize(image,(80,160,3))
    small_img=np.array(small_img)
    small_img=small_img[None,:,:,:] #adding a dimension for prediction

    prediction=model.predict(small_img)[0]*255
    lanes.recent_fit.append(prediction)

    if len(lanes.recent_fit)>5:
      lanes.recent_fit= lanes.recent_fit[1:]

    lanes.avg_fit=np.mean(np.array([i for i in lanes.recent_fit]),axis=0)

    blanks= np.zeros_like(lanes.avg_fit).astype(np.uint8)
    lane_drawn = np.dstack((blanks, lanes.avg_fit,blanks))

    lane_image=resize(lane_drawn, (720,1280,3) )

    result = cv2.addWeighted(image, 1, lane_image.astype(np.uint8), 1, 0)

    return result



uploaded=files.upload()

vid_input= VideoFileClip("lanes_clip.mp4")
vid_output= 'lanes_output_clip.mp4'
lanes= Lanes()

vid_clip= vid_input.fl_image(road_lines)
vid_clip.write_videofile(vid_output)