#Author: Kartik Bharadwaj

import cv2
import numpy as np
import os

def main():

    capture = cv2.VideoCapture(0)                     

    if capture.isOpened() == False:                           
        print "error: Camera not accessed\n"
        break

    while cv2.waitKey(1) != 27 and capture.isOpened():
        imgOrg = capture.read()

        if not imgOrg is None:             
            print "error: frame not read from camera\n"
            break

        imgHSV = cv2.cvtColor(imgOrg, cv2.COLOR_BGR2HSV)

        Thresholdlow = cv2.inRange(imgHSV, (0, 155, 155), (18, 255, 255))
        Thresholdhigh = cv2.inRange(imgHSV, (165, 155, 155), (179, 255, 255))

        ThreshAdd = cv2.add(Thresholdlow, Thresholdhigh)

        imgGblur = cv2.GaussianBlur(ThreshAdd, (5, 5), 1)               

        imgGblur = cv2.dilate(imgGblur, np.ones((22,22),np.uint8))        
        imgGblur = cv2.erode(imgGblur, np.ones((8,8),np.uint8))   

        Rows, Columns = imgGblur.shape        

        circles = cv2.HoughCircles(imgGblur, cv2.HOUGH_GRADIENT, 2, Rows / 4)      

        if circles is not None:                    
            for circle in circles[0]:                      
                x, y, rad = circle
                print "Zone x = " + str(x) + ", y = " + str(y) + ", rad = " + str(rad)
                cv2.circle(imgOrg, (x, y), 3, (0, 255, 0), cv2.FILLED)
                cv2.circle(imgOrg, (x, y), rad, (0, 0, 255), 3)

        cv2.imshow("Original frame", imgOrg)            
        cv2.imshow("Threshold frame", imgGblur)
    # end while

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()