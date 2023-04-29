# -*- coding: utf-8 -*-
"""
Shape Detection UI

Created on Sat Apr 29 2023

@author: Nonpawit Ekburanawat
"""
        
import tkinter as tk
from   tkinter import filedialog
from   PIL     import Image, ImageTk
import cv2     as cv
import numpy   as np
import os.path

def upload_file():
    global _video, raw, detect, photo
    
    if _video:
        _video = False
    
    file_types = [('Video Files', '*.avi;*.mp4;*.mov;*.mkv'), 
                  ('Photo Files', '*.jpg;*.png')]
    file_path  = filedialog.askopenfilename(filetypes=file_types)
    
    if file_path:
        file_ext = os.path.splitext(file_path)[1]
        if file_ext.lower() in ('.avi', '.mp4', '.mov', '.mkv'):
            _video = True
            video_canvas(file_path)
        elif file_ext.lower() in ('.jpg', '.jpeg', '.png'):
            img = cv.imread(file_path)
            
            img     = cv.resize(img, (712, 400))
            contour = img.copy()
            img     = cv.cvtColor(img, cv.COLOR_BGR2RGB)
            
            blur = cv.GaussianBlur(img, (7, 7), 1)
            gray = cv.cvtColor(blur, cv.COLOR_BGR2GRAY)
            
            t1 = thr1.get()
            t2 = thr2.get()
            
            canny   = cv.Canny(gray, t1, t2)
            kernel  = np.ones((10, 10))
            dil     = cv.dilate(canny, kernel, iterations=1)
            
            photo = ImageTk.PhotoImage(Image.fromarray(img))
            raw.create_image(0, 0, image=photo, anchor=tk.NW)
            detect.create_image(0, 0, image=photo, anchor=tk.NW)
            
            find_contour(dil, contour)
            
            raw.update()
            detect.update()
    
    return

def open_cam():
    global _video
    
    if camera['text'] == "Open Camera":
        _video = True
        camera.config(text="Close Camera")
        video_canvas(0)
    elif camera['text'] == "Close Camera":
        _video = False
        camera.config(text="Open Camera")
    
    
    return

def video_canvas(source):
    global _video
    
    cap = cv.VideoCapture(source)
    
    while cap.isOpened() & _video:
        ret, img = cap.read()
        
        if not ret:
            break
        
        img     = cv.resize(img, (712, 400))
        contour = img.copy()
        img     = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        
        blur = cv.GaussianBlur(img, (7, 7), 1)
        gray = cv.cvtColor(blur, cv.COLOR_BGR2GRAY)
        
        t1 = thr1.get()
        t2 = thr2.get()
        
        canny   = cv.Canny(gray, t1, t2)
        kernel  = np.ones((10, 10))
        dil     = cv.dilate(canny, kernel, iterations=1)
        
        photo = ImageTk.PhotoImage(Image.fromarray(img))
        raw.create_image(0, 0, image=photo, anchor=tk.NW)
        detect.create_image(0, 0, image=photo, anchor=tk.NW)
        
        find_contour(dil, contour)
        
        raw.update()
        detect.update()
    
    raw.delete("all")
    detect.delete("all")
    return

def find_contour(dil, img):
    contours, _ = cv.findContours(dil, 
                                  cv.RETR_EXTERNAL, 
                                  cv.CHAIN_APPROX_NONE)
    
    detect.delete("rect")
    detect.delete("indicate")
    for cnt in contours:
        areaMin = int(size.get())
        area = cv.contourArea(cnt)

        if area > areaMin:
            approx = cv.approxPolyDP(cnt, 
                                     0.04 * cv.arcLength(cnt, True), 
                                     True)
            x, y, w, h = cv.boundingRect(approx)
            
            detect.create_rectangle(x, y, 
                                    x + w, y + h, 
                                    outline='green', 
                                    width=3, 
                                    tag="rect")
    
            edges = len(approx)
            if edges == 3:
                detect.create_text(x + w + 40, 
                                   y + 65, 
                                   text="Triangle",
                                   fill='blue',
                                   font=("Arial", 13),
                                   tag="indicate")
            elif edges == 4:
                detect.create_text(x + w + 40, 
                                   y + 65, 
                                   text="Rectangles",
                                   fill='blue',
                                   font=("Arial", 13),
                                   tag="indicate")
            elif edges == 5:
                detect.create_text(x + w + 40, 
                                   y + 45, 
                                   text="Pentagon",
                                   fill='blue',
                                   font=("Arial", 13),
                                   tag="indicate")
            elif edges == 6:
                detect.create_text(x + w + 40, 
                                   y + 45, 
                                   text="Hexagon",
                                   fill='blue',
                                   font=("Arial", 13),
                                   tag="indicate")
            else:
                detect.create_text(x + w + 40, 
                                   y + 45, 
                                   text="Circle",
                                   fill='blue',
                                   font=("Arial", 13),
                                   tag="indicate")
    

## Initialize Window Settting
_video = False
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
thr1.set(100)

thr2   = tk.Scale(right_frame, 
                  from_=0, 
                  to=255, 
                  length=285,
                  orient=tk.HORIZONTAL)
thr2.pack(side=tk.TOP)
thr2.set(200)

size   = tk.Scale(right_frame, 
                  from_=0, 
                  to=20000, 
                  length=285,
                  orient=tk.HORIZONTAL)
size.pack(side=tk.TOP)
size.set(2000)

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
                command=open_cam)
camera.pack(side=tk.TOP)

root.mainloop()