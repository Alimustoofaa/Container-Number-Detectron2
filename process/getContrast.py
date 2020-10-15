import cv2
import numpy as np

def getContrast(img):
  lab = cv2.cvtColor(img,cv2.COLOR_BGR2LAB)

  # separate channels
  L,A,B=cv2.split(lab)

  # compute minimum and maximum in 5x5 region using erode and dilate
  kernel = np.ones((5,5),np.uint8)
  min = cv2.erode(L,kernel,iterations = 1)
  max = cv2.dilate(L,kernel,iterations = 1)

  # convert min and max to floats
  min = min.astype(np.float64) 
  max = max.astype(np.float64) 

  # compute local contrast
  contrast = (max-min)/(max+min)

  # get average across whole image
  average_contrast = 100*np.mean(contrast)

  return round(average_contrast, 2)