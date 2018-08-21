import cv2
import numpy as np
from LogKey import key_check
import time 
from PIL import ImageGrab


hash_dict = {'W':0, 'S':1, 'A':2, 'D':3, 'B':4, 'V':5}
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

time.sleep(20)
print("Logging Started\n")
while True:
    printscreen =  np.array(ImageGrab.grab(bbox=(0,40,800,640)))
    printscreen = process_img(printscreen)
    keys = key_check()
    if "Q" in keys:
        break;
    one_hot = [0,0,0,0,0,0]
    for u in hash_dict.keys():
        if u in keys:
            one_hot[hash_dict[u]] = 1
    print(one_hot)
    X.append(printscreen)
    y.append(one_hot)
np.save("X.npy",X)
np.save("Y.npy",y)

