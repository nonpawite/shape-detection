# -*- coding: utf-8 -*-
"""
Computer Vision Project :
    Post Processing Test

Created on Wed Apr 12 2023

@author: Nonpawit Ekburanawat
"""

import cv2               as cv
import numpy             as np
import matplotlib.pyplot as plt

img  = cv.imread('./test_data/shapes.png')
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)