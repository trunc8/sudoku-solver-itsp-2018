# Import the modules
import cv2
import numpy as np
import imutils
import os

from sklearn.externals import joblib
from skimage.feature import hog
from skimage import io
from matplotlib import pyplot as plt

# Take an image
#os.system("raspistill -o final.jpg")



# Load the classifier
clf = joblib.load("digits_cls.pkl")

print("chk1")

# Read the input image
im_path = "final.jpg"
im = cv2.imread(im_path)
im_c = cv2.imread(im_path)
im_d = cv2.imread(im_path)
a,b,_ = im.shape
im = im[(81*a)//288:(82*a)//128, (97*b)//288:(39*b)//64]
start_y = (9*a)//48
len_y = (9*a)//16 - (9*a)//48
start_x = (46*a)//144
len_y = (19*a)//32 - (46*a)//144
a,b,_ = im.shape

print("chk2")

# Denoising image
im = cv2.fastNlMeansDenoising(im, 11, 31, 9)

print("chk3")

rot = 0
im = imutils.rotate(im, rot)
im_d = imutils.rotate(im_d, rot)

print("chk4")
#im = im_copy[(2*a)//7:a, b//10:(5*b)//7] 
#cv2.imwrite("tt.jpg",imm)
#cv2.imwrite("t.jpg",im)

# Convert to grayscale and apply filtering
im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

#im_gray = cv2.GaussianBlur(im_gray, (5, 5), 0)

print("chk5")

# Threshold the image
ret,im_th = cv2.threshold(im_gray,100,255,cv2.THRESH_BINARY_INV)
#im_th = cv2.adaptiveThreshold(im_gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
#im_th = cv2.adaptiveThreshold(im_gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)

plt.imshow(im_th, cmap='gray', interpolation = 'bicubic')
plt.show()

#die()
#sys.exit()
# Find contours in the image
_,ctrs, hier = cv2.findContours(im_th.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Get rectangles contains each contour
rects = [cv2.boundingRect(ctr) for ctr in ctrs]

#unsolved = [[0 for x in range (9)] for y in range (9)]
unsolved = np.zeros((9,9))

print("chk6")

# For each rectangular region, calculate HOG features and predict
# the digit using Linear SVM.
for rect in rects:
    # Draw the rectangles
    cv2.rectangle(im, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (0, 255, 0), 3)
    #print(rect[0], rect[1])
    # Make the rectangular region around the digit
    leng = int(rect[3] * 1.6)
    pt1 = int(rect[1] + rect[3] // 2 - leng // 2)
    pt2 = int(rect[0] + rect[2] // 2 - leng // 2)
    if pt1<=0 or pt2<=0:
        continue 
    roi = im_th[pt1:pt1+leng, pt2:pt2+leng]
    # Resize the image
    roi = cv2.resize(roi, (28, 28), interpolation=cv2.INTER_AREA)
    roi = cv2.dilate(roi, (3, 3))
    # Calculate the HOG features
    roi_hog_fd = hog(roi, orientations=9, pixels_per_cell=(14, 14), cells_per_block=(1, 1), visualise=False)
    nbr = (clf.predict(np.array([roi_hog_fd], 'float64')))
    #print(nbr)
    for i in range (0,9):
        for j in range (0,9):
            if rect[0]>(b*i)//9 and rect[0]<(b*(i+1))//9 and rect[1]>(a*j)//9 and rect[1]<(a*(j+1))//9:
                unsolved[j][i] = nbr
    cv2.putText(im, str(int(nbr[0])), (rect[0], rect[1]),cv2.FONT_HERSHEY_DUPLEX, 2, (0, 255, 255), 3)

for i in range (0,9):
    print(unsolved[i])
plt.imshow(im, cmap = 'gray', interpolation = 'bicubic')
plt.show()
#cv2.waitKey(0)
#solveSudoku(unsolved)
#print(unsolved)
def recognize():
    return unsolved

