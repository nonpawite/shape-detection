import tkinter as tk
from tkinter import filedialog
from tkinter.filedialog import askopenfile
from PIL import Image, ImageTk
import subprocess
import cv2 as cv

my_w = tk.Tk()

def upload_file():
    global img, img_tk, result_tk
    #f_types = [('Jpg Files', '*.jpg'), ('Png Files', '*.png')]
    filename = filedialog.askopenfilename(filetypes=[])
    img = cv.imread(filename)

    # Apply shape detection
    gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    gray = gray_img
    _, thresh_image = cv.threshold(gray, 220, 255, cv.THRESH_BINARY)
    contours, hierarchy = cv.findContours(thresh_image, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    for i, contour in enumerate(contours):
        if i == 0:
            continue

        epsilon = 0.01*cv.arcLength(contour, True)
        approx = cv.approxPolyDP(contour, epsilon, True)

        cv.drawContours(img, contour, 0, (0,0,0), 4)

        x,y,w,h = cv.boundingRect(approx)
        x_mid = int(x + w/3)
        y_mid = int(y + h/1.5)

        coords = (x_mid, y_mid)
        colour = (0,0,0)
        font = cv.FONT_HERSHEY_DUPLEX

        if len(approx) == 3:
            cv.putText(img, "Triangle", coords, font, 1, colour, 1)
        elif len(approx) == 4:
            cv.putText(img, "Quadilateral", coords, font, 1, colour, 1)
        elif len(approx) == 5:
            cv.putText(img, "Pentagon", coords, font, 1, colour, 1)
        elif len(approx) == 6:
            cv.putText(img, "Hexagon", coords, font, 1, colour, 1)
        else:
            cv.putText(img, "Circle", coords, font, 1, colour, 1)

    # Convert the image to a Tkinter PhotoImage and display it in the UI
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    img = img.resize((800,600))
    img_tk = ImageTk.PhotoImage(img)
    b2 = tk.Button(my_w, image=img_tk, bd = 0, highlightthickness=0, relief='flat')
    b2.image_names = img_tk
    b2.grid(row=3, column=1)

    # resize the window to fit the uploaded image
    width, height = img.size
    my_w.geometry(f"{width+200}x{height+200}")

def video_preview():
    subprocess.Popen(["python", "test.py"])

my_w.geometry("1280x720")
my_w.title('SHAPE DETECTION')
my_font1=('times', 18, 'bold')

l1 = tk.Label(my_w, text='IMAGE SHAPE DETECTION', font=my_font1)
l1.grid(row=1, column=1, padx=10, pady=50, sticky="nsew")

b1 = tk.Button(my_w, text='Upload File', width=20, command=upload_file, bd = 0, highlightthickness=0, relief='flat')
b1.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

l3 = tk.Label(my_w, text='VIDEO SHAPE DETECTION', font=my_font1)
l3.grid(row=4, column=1, padx=10, pady=50, sticky="nsew")

b3 = tk.Button(my_w, text='Open Camera', width=20, command=video_preview, bd = 0, highlightthickness=0, relief='flat')
b3.grid(row=5, column=1, padx=10, pady=10, sticky="nsew")

my_w.grid_rowconfigure(0, weight=1)
my_w.grid_rowconfigure(6, weight=1)
my_w.grid_columnconfigure(0, weight=1)
my_w.grid_columnconfigure(2, weight=1)

my_w.mainloop()