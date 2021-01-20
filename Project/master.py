# Import of required directories
import RPi.GPIO as GPIO
import numpy as np
import cv2
import imutils
import sys
import os

from sklearn.externals import joblib
from skimage.feature import hog
from skimage import io
from matplotlib import pyplot as plt
from time import sleep
from motorCode import move_stepper_x, move_stepper_y, move_numwheel
from solve import solveSudoku
from performRecognition import recognize


clf = joblib.load("digits_cls.pkl")


# Variable/Pin declarations,X is lower stepper, Y is upper stepper, clockwise assumed forward.
CW = 0
ACW = 1
XDirPin = 16
XStepPin = 18
YDirPin = 38
YStepPin = 40
RnPPWMPin = 12
NumPWMPin = 11
StepsPerBlock = 50
Delay = 0.0008
beg = 2.6
end = 6.85
initial_x = 0
initial_y = 370

# GPIO Setup
GPIO.setmode(GPIO.BOARD)
GPIO.setup(XDirPin, GPIO.OUT)
GPIO.setup(XStepPin, GPIO.OUT)
GPIO.setup(YDirPin, GPIO.OUT)
GPIO.setup(YStepPin, GPIO.OUT)
GPIO.setup(RnPPWMPin, GPIO.OUT)
GPIO.setup(NumPWMPin, GPIO.OUT)

# PWM Setup
pwmNum = GPIO.PWM(NumPWMPin,50)
pwmNum.start(7)
pwmRnP = GPIO.PWM(RnPPWMPin,50)
pwmRnP.start(4) 

# giving an unsolved sudoku
unsolved = recognize()

#solving the sudoku
solved_flipped_transposed = np.zeros((9,9))
solved_flipped = np.zeros((9,9))
unsolved_flipped = np.zeros((9,9))
solved = np.zeros((9,9))
for i in range (0,9):
    for j in range (0,9):
        solved_flipped_transposed[i][j] = unsolved[i][j]
solveSudoku(solved_flipped_transposed)
for i in range (0,9):
    for j in range (0,9):
        solved_flipped[i][j] = solved_flipped_transposed[j][i]
for i in range (0,9):
    for j in range (0,9):
        solved[i][j] = solved_flipped[8-i][j]

for i in range (0,9):
    for j in range (0,9):
        unsolved_flipped[i][j] = unsolved[j][i]
for i in range (0,9):
    for j in range (0,9):
        unsolved[i][j] = unsolved_flipped[8-i][j]
        
print("Unsolved Sudoku")
print(unsolved)
print("Solved Sudoku")
print(solved)

#initial setup
#XStepCount = move_stepper_x(0,2.3)
GPIO.output(XDirPin, CW)
for x in range(0,initial_x):
    GPIO.output(XStepPin, GPIO.HIGH)
    sleep(Delay)
    GPIO.output(XStepPin, GPIO.LOW)
    sleep(Delay)
sleep(0.1)

GPIO.output(YDirPin, CW)
#YStepCount = move_stepper_y(0,2.75)
for y in range(0,initial_y):
    GPIO.output(YStepPin, GPIO.HIGH)
    sleep(Delay)
    GPIO.output(YStepPin, GPIO.LOW)
    sleep(Delay) 
sleep(0.1)

prev_x = 0
prev_y = 0

# moving the motors
for i in range (0,9):
    for j in range (0,9):
        if unsolved[i][j] == 0:
            cur_x = i
            cur_y = j
            '''print(prev_x)
            print(prev_y)
            print(cur_x)
            print(cur_y)'''
            if(cur_x >= prev_x):
                GPIO.output(XDirPin, CW)
                XStepCount = move_stepper_x(prev_x, cur_x)
                for x in range(XStepCount):
                    GPIO.output(XStepPin, GPIO.HIGH)
                    sleep(Delay)
                    GPIO.output(XStepPin, GPIO.LOW)
                    sleep(Delay)
                print("stepper x moved to")
                print(cur_x)
                sleep(0.1)
            
            if(cur_x < prev_x):
                GPIO.output(XDirPin, ACW)
                XStepCount = -move_stepper_x(prev_x, cur_x)
                for x in range(XStepCount):
                    GPIO.output(XStepPin, GPIO.HIGH)
                    sleep(Delay)
                    GPIO.output(XStepPin, GPIO.LOW)
                    sleep(Delay)
                print("stepper x moved to")
                print(cur_x)    
                sleep(0.1)
            
            if(cur_y >= prev_y):
                GPIO.output(YDirPin, CW)
                YStepCount = move_stepper_y(prev_y, cur_y)
                print("YStep")
                print(YStepCount)
                for y in range(YStepCount):
                    GPIO.output(YStepPin, GPIO.HIGH)
                    sleep(Delay)
                    GPIO.output(YStepPin, GPIO.LOW)
                    sleep(Delay)
                print("stepper y moved to")
                print(cur_y)    
                sleep(0.1)
            
            if(cur_y < prev_y):
                GPIO.output(YDirPin, ACW)
                YStepCount = move_stepper_y(prev_y, cur_y)
                YStepCount = -YStepCount
                print("YStep")
                print(YStepCount)
                for y in range(YStepCount):
                    GPIO.output(YStepPin, GPIO.HIGH)
                    sleep(Delay)
                    GPIO.output(YStepPin, GPIO.LOW)
                    sleep(Delay)
                print("stepper y moved to")
                print(cur_y)    
                sleep(0.1)
            
            #number wheel
            DC = move_numwheel(solved[i][j])
            temp = (solved[i][j]+5)%9
            DC_temp = move_numwheel(temp)
            pwmNum.ChangeDutyCycle(DC_temp)
            sleep(0.35) 
            pwmNum.ChangeDutyCycle(DC)
            print("Number printed is ")
            print(solved[i][j])
            
            if solved[i][j]==8 or solved[i][j]==9:
                GPIO.output(YDirPin, ACW)
                YStepCount = move_stepper_y(0, 0.5)
                for y in range(int(YStepCount)):
                    GPIO.output(YStepPin, GPIO.HIGH)
                    sleep(Delay)
                    GPIO.output(YStepPin, GPIO.LOW)
                    sleep(Delay)
            
            if solved[i][j]==1:
                GPIO.output(YDirPin, ACW)
                YStepCount = move_stepper_y(0, 0.4)
                for y in range(int(YStepCount)):
                    GPIO.output(YStepPin, GPIO.HIGH)
                    sleep(Delay)
                    GPIO.output(YStepPin, GPIO.LOW)
                    sleep(Delay)
                    
            if solved[i][j]==2:
                GPIO.output(YDirPin, ACW)
                YStepCount = move_stepper_y(0, 0.2)
                for y in range(int(YStepCount)):
                    GPIO.output(YStepPin, GPIO.HIGH)
                    sleep(Delay)
                    GPIO.output(YStepPin, GPIO.LOW)
                    sleep(Delay)
                    
            #Rack and Pinion
            for m in range (0,90):
                DC = beg + ((end-beg)*m)/90
                pwmRnP.ChangeDutyCycle(DC)
                sleep(0.05)

            sleep(0.1)

            for n in range (90,0,-1):
                DC = beg+((end-beg)*n)/90
                pwmRnP.ChangeDutyCycle(DC)
                sleep(0.05)
            
            sleep(0.1)
            print("Rack and pinion moved")
            print("")
            
            if solved[i][j]==8 or solved[i][j]==9:
                GPIO.output(YDirPin, CW)
                YStepCount = move_stepper_y(0, 0.5)
                for y in range(int(YStepCount)):
                    GPIO.output(YStepPin, GPIO.HIGH)
                    sleep(Delay)
                    GPIO.output(YStepPin, GPIO.LOW)
                    sleep(Delay)
                    
            if solved[i][j]==1:
                GPIO.output(YDirPin, CW)
                YStepCount = move_stepper_y(0, 0.4)
                for y in range(int(YStepCount)):
                    GPIO.output(YStepPin, GPIO.HIGH)
                    sleep(Delay)
                    GPIO.output(YStepPin, GPIO.LOW)
                    sleep(Delay)
                    
            if solved[i][j]==2:
                GPIO.output(YDirPin, CW)
                YStepCount = move_stepper_y(0, 0.2)
                for y in range(int(YStepCount)):
                    GPIO.output(YStepPin, GPIO.HIGH)
                    sleep(Delay)
                    GPIO.output(YStepPin, GPIO.LOW)
                    sleep(Delay)
                    
            prev_x = cur_x
            prev_y = cur_y

GPIO.output(YDirPin, ACW)
YStepCount = move_stepper_y(8,0)
YStepCount = -YStepCount
for y in range(YStepCount):
    GPIO.output(YStepPin, GPIO.HIGH)
    sleep(Delay)
    GPIO.output(YStepPin, GPIO.LOW)
    sleep(Delay)

#Cleanup
pwmNum.stop()
pwmRnP.stop()
GPIO.cleanup()
