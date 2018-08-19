from tkinter import *
from PIL import ImageGrab
import numpy as np
import cv2
import time
import pyautogui as pg
import DirectInputRoutines as DIR
from LogKey import key_check
last_time = time.time()
one_hot = [0, 0, 0, 0]
hash_dict = {'w':0, 's':1, 'a':2, 'd':3}
X = []
y = []


def auto_canny(image, sigma=0.33):
	# compute the median of the single channel pixel intensities
	v = np.median(image)
	# apply automatic Canny edge detection using the computed median
	lower = int(max(0, (1.0 - sigma) * v))
	upper = int(min(255, (1.0 + sigma) * v))
	edged = cv2.Canny(image, lower, upper)
	# return the edged image
	return edged
def process_img(original_image):
    processed_img = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    processed_img = cv2.Canny(processed_img, threshold1=200, threshold2=300)
    processed_img = cv2.Canny(processed_img, threshold1=200, threshold2=300)
    #processed_img = cv2.Canny(processed_img, threshold1=200, threshold2=300)
    
    vertices = np.array([[10,500],[10,300],[300,200],[500,200],[800,300],[800,500],
                         ], np.int32)

    processed_img = cv2.GaussianBlur(processed_img,(5,5),0)
    processed_img = roi(processed_img, [vertices])

    # more info: http://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_houghlines/py_houghlines.html
    #                          edges       rho   theta   thresh         # min length, max gap:        
    #lines = cv2.HoughLinesP(processed_img, 1, np.pi/180, 180,      20,         15)
    #draw_lines(processed_img,lines)
    return processed_img


def roi(img, vertices):
    #blank mask:
    mask = np.zeros_like(img)
    # fill the mask
    cv2.fillPoly(mask, vertices, 255)
    # now only show the area that is the mask
    masked = cv2.bitwise_and(img, mask)
    return masked


def draw_lines(img,lines):
    for line in lines:
        coords = line[0]
        cv2.line(img, (coords[0], coords[1]), (coords[2], coords[3]), [255,255,255], 3)

def change_tab():
    pg.hotkey("alt","tab")
def send_key(e):
    hash = {"w":DIR.W, "a":DIR.A, "s":DIR.S, "d":DIR.D}
    return hash[e.keysym]
def keyup(e):
    
    if(e.keysym == "Alt_L" or e.keysym == "Tab"):
        return
    #print('down', e.keysym)
    change_tab()
    DIR.ReleaseKey(send_key(e))
    change_tab()
    global last_time
    one_hot[hash_dict[e.keysym]] = 0
    temp = list(one_hot)
    printscreen =  np.array(ImageGrab.grab(bbox=(0,40,800,640)))
    printscreen = process_img(printscreen)
    print('loop took {} seconds'.format(time.time()-last_time))
    print([printscreen, temp])
    last_time = time.time()
    X.append(printscreen)
    y.append(temp)
    #cv2.imshow("image", printscreen)

def keydown(e):
    #print('up', e.keysym)
    if(e.keysym == "Alt_L" or e.keysym == "Tab"):
        return
    change_tab()
    DIR.ReleaseKey(send_key(e))
    change_tab()
    global last_time
    one_hot[hash_dict[e.keysym]] = 1
    temp = list(one_hot)
    printscreen =  np.array(ImageGrab.grab(bbox=(0,40,800,640)))
    printscreen = process_img(printscreen)
    print('loop took {} seconds'.format(time.time()-last_time))
    print([printscreen,temp])
    last_time = time.time()
    X.append(printscreen)
    y.append(temp)

root = Tk()
frame = Frame(root, width=100, height=100)
frame.bind("<KeyPress>", keydown)
frame.bind("<KeyRelease>", keyup)
frame.pack()
frame.focus_set()
root.mainloop()
np.save("X.npy", X)
np.save("y.npy", y)