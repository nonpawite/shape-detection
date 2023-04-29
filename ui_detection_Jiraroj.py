# -*- coding: utf-8 -*-
"""
Created on Sat Apr 29 00:39:11 2023

@author: nonpa
@editor: Jiraroj
"""
        
import tkinter as tk
from   tkinter import filedialog
from   PIL     import Image, ImageTk
import cv2     as cv
import numpy   as np
import os.path
import subprocess


def upload_file():    
    file_types = [('Video Files', '*.avi;*.mp4;*.mov;*.mkv'), 
                  ('Photo Files', '*.jpg;*.png')]
    file_path  = filedialog.askopenfilename(filetypes=file_types)
    
    if file_path:
        file_ext = os.path.splitext(file_path)[1]
        if file_ext.lower() in ('.avi', '.mp4', '.mov', '.mkv'):
            cap = cv.VideoCapture(file_path)
            while cap.isOpened():
                ret, img  = cap.read()
                
                if not ret:
                    break
                
                img     = cv.resize(img, (712, 400))
                img     = cv.cvtColor(img, cv.COLOR_BGR2RGB)
                photo   = ImageTk.PhotoImage(Image.fromarray(img))
                raw.create_image(0, 0, image=photo, anchor=tk.NW)
                detect.create_image(0, 0, image=photo, anchor=tk.NW)
                raw.update()
                
                blur = cv.GaussianBlur(img, (7, 7), 1)
                gray = cv.cvtColor(blur, cv.COLOR_BGR2GRAY)
                
                t1 = 100
                t2 = 200
                
                canny = cv.Canny(gray, t1, t2)
                
                kernel  = np.ones((10, 10))
                dil     = cv.dilate(canny, kernel, iterations=1)
                contour = img.copy()
                
                find_contour(dil, contour)
                detect.update()

        elif file_ext.lower() in ('.jpg', '.jpeg', '.png'):
            img = cv.imread(file_path)
            img = cv.resize(img, (712, 400))
            img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
            photo = ImageTk.PhotoImage(Image.fromarray(img))
            raw.create_image(0, 0, image=photo, anchor=tk.NW)
            detect.config(width=img.shape[1], height=img.shape[0])
            detect.create_image(0, 0, image=photo, anchor=tk.NW)
            
            blur = cv.GaussianBlur(img, (7, 7), 1)
            gray = cv.cvtColor(blur, cv.COLOR_BGR2GRAY)

            t1 = thr1.get()
            t2 = thr2.get()

            canny = cv.Canny(gray, t1, t2)

            kernel = np.ones((10, 10))
            dil = cv.dilate(canny, kernel, iterations=1)
            contour = img.copy()

            # Shape detection
            gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
            _, thresh = cv.threshold(gray, 127, 255, cv.THRESH_BINARY_INV)
            contours, _ = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

            for cnt in contours:
                approx = cv.approxPolyDP(cnt, 0.01*cv.arcLength(cnt, True), True)
                x = approx.ravel()[0]
                y = approx.ravel()[1]
                
                if len(approx) == 3:
                    cv.drawContours(img, [approx], 0, (0, 255, 0), 5)
                    cv.putText(img, "Triangle", (x, y), cv.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0))
                elif len(approx) == 4:
                    cv.drawContours(img, [approx], 0, (0, 255, 0), 5)
                    cv.putText(img, "Rectangle", (x, y), cv.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0))
                elif len(approx) == 5:
                    cv.drawContours(img, [approx], 0, (0, 255, 0), 5)
                    cv.putText(img, "Pentagon", (x, y), cv.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0))
                elif len(approx) == 6:
                    cv.drawContours(img, [approx], 0, (0, 255, 0), 5)
                    cv.putText(img, "Hexagon", (x, y), cv.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0))
                elif len(approx) == 7:
                    cv.drawContours(img, [approx], 0, (0, 255, 0), 5)
                    cv.putText(img, "Heptagon", (x, y), cv.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0))
                elif len(approx) == 8:
                    cv.drawContours(img, [approx], 0, (0, 255, 0), 5)
                    cv.putText(img, "Octagon", (x, y), cv.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0))
                elif len(approx) == 9:
                    cv.drawContours(img, [approx], 0, (0, 255, 0), 5)
                    cv.putText(img, "Nonagon", (x, y), cv.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0))
                else:
                    cv.drawContours(img, [approx], 0, (0, 255, 0), 5)
                    cv.putText(img, "Circle", (x, y), cv.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0))

            raw.image = photo
            raw.create_image(0, 0, image=photo, anchor=tk.NW)

            img = cv.cvtColor(img, cv.COLOR_RGB2BGR)
            photo = ImageTk.PhotoImage(Image.fromarray(img))
            detect.create_image(0, 0, image=photo, anchor=tk.NW)
            detect.image = photo
            detect.update()

        else:
            print("No file selected")

def find_contour(dil, img):
    contours, _ = cv.findContours(dil, 
                                  cv.RETR_EXTERNAL, 
                                  cv.CHAIN_APPROX_NONE)
    
    for cnt in contours:
        areaMin = int(size.get())
        area = cv.contourArea(cnt)

        if area > areaMin:
            cv.drawContours(img, cnt, -1, (255, 0, 0), 3)
            peri = cv.arcLength(cnt, True)
            approx = cv.approxPolyDP(cnt, 0.02 * peri, True)
            x, y, w, h = cv.boundingRect(approx)
            
            detect.create_rectangle(x, y, 
                                    x + w, y + h, 
                                    outline='green', 
                                    width=3)
    
            edges = len(approx)
            if edges == 3:
                detect.create_text(x + w + 40, 
                                   y + 65, 
                                   text="Triangle",
                                   fill='blue',
                                   font=("Arial", 13))
            elif edges == 4:
                detect.create_text(x + w + 40, 
                                   y + 65, 
                                   text="Rectangles",
                                   fill='blue',
                                   font=("Arial", 13))
            elif edges == 5:
                detect.create_text(x + w + 40, 
                                   y + 45, 
                                   text="Pentagon",
                                   fill='blue',
                                   font=("Arial", 13))
            elif edges == 6:
                detect.create_text(x + w + 40, 
                                   y + 45, 
                                   text="Hexagon",
                                   fill='blue',
                                   font=("Arial", 13))
            else:
                detect.create_text(x + w + 40, 
                                   y + 45, 
                                   text="Circle",
                                   fill='blue',
                                   font=("Arial", 13))
    
def video_preview():
    subprocess.Popen(["python", "test.py"])

## Initialize Window Settting
root = tk.Tk()
root.geometry("1000x800")
root.title("Shape Detection")
root.resizable(False, False)

vdo_frame = tk.Frame(root)
vdo_frame.pack(side=tk.LEFT)

raw    = tk.Canvas(vdo_frame, 
                   width=712, 
                   height=400, 
                   bg='lightgray')
raw.pack(side=tk.TOP)

detect = tk.Canvas(vdo_frame, 
                   width=712, 
                   height=400, 
                   bg='lightgray')
detect.pack(side=tk.TOP)

right_frame = tk.Frame(root)
right_frame.pack(side=tk.LEFT)

thr1   = tk.Scale(right_frame, 
                  from_=0, 
                  to=255, 
                  length=285,
                  orient=tk.HORIZONTAL)
thr1.pack(side=tk.TOP)

thr2   = tk.Scale(right_frame, 
                  from_=0, 
                  to=255, 
                  length=285,
                  orient=tk.HORIZONTAL)
thr2.pack(side=tk.TOP)

size   = tk.Scale(right_frame, 
                  from_=0, 
                  to=20000, 
                  length=285,
                  orient=tk.HORIZONTAL)
size.pack(side=tk.TOP)

tk.Frame(right_frame, 
         height=30,
         bd=0,
         relief="ridge") \
    .pack(side=tk.TOP)

upload = tk.Button(right_frame, 
                text='Upload File', 
                width=20, 
                command=upload_file)
upload.pack(side=tk.TOP)


camera = tk.Button(right_frame, 
                text='Open Camera', 
                width=20, 
                command=video_preview)
camera.pack(side=tk.TOP)

root.mainloop()