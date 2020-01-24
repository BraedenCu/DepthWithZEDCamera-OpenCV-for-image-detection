import sys
import numpy as np
import pyzed.sl as sl
import cv2

def detect():
    lowerBound=np.array([33,80,40])
    upperBound=np.array([102,255,255])
    red = (255,0,0)
    distance = 1
    xcenter = 1
    center = 0

    kernelOpen=np.ones((5,5))
    kernelClose=np.ones((20,20))

    # Create an RGBA sl.Mat object
    image_zed = sl.Mat(zed.get_resolution().width, zed.get_resolution().height, sl.MAT_TYPE.MAT_TYPE_8U_C4)
    # Retrieve data in a numpy array with get_data()
    image_ocv = image_zed.get_data()

    # Create an RGBA sl.Mat object
    image_depth_zed = sl.Mat(zed.getResolution().width, sl.get_resolution().height, sl.MAT_TYPE.MAT_TYPE_8U_C4)

    if zed.grab() == SUCCESS :
        # Retrieve the left image in sl.Mat
        zed.retrieve_image(image_zed, sl.VIEW.VIEW_LEFT)
        # Use get_data() to get the numpy array
        image_ocv = image_zed.get_data()
        # Display the left image from the numpy array
        cv2.imshow("Image", image_ocv)
        # Retrieve depth data (32-bit)
        zed.retrieve_measure(depth_zed, sl.MEASURE.MEASURE_DEPTH)
        # Load depth data into a numpy array
        depth_ocv = depth_zed.get_data()
        # Print the depth value at the center of the image
        # print(depth_ocv[int(len(depth_ocv)/2)][int(len(depth_ocv[0])/2)])
        # Retrieve the normalized depth image
        zed.retrieve_image(image_depth_zed, sl.VIEW.VIEW_DEPTH)
        # Use get_data() to get the numpy array
        image_depth_ocv = image_depth_zed.get_data()
        # Display the depth view from the cv::Mat object
        cv2.imshow("Image", image_depth_ocv)

    ret, image = image_ocv.read()
    #resize function
    frame = cv2.resize(image, (250, 250))
    
    #convert BGR to HSV
    imgHSV = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    # create the Mask
    mask=cv2.inRange(imgHSV,lowerBound,upperBound)
    #morphology
    maskOpen=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernelOpen)
    maskClose=cv2.morphologyEx(maskOpen,cv2.MORPH_CLOSE,kernelClose)

    maskFinal=maskClose
    _, conts, _= cv2.findContours(maskFinal.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for i in range(len(conts)):
        #cool center stuff (for big brains only)        
        c =  max(conts,key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        if radius > 50:
             x,y,w,h=cv2.boundingRect(conts[i])
             cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255), 2)
             print(center)
             xcenter = (int(M["m10"] / M["m00"]))
             distance = int(xcenter - 125)
        else:
             break
    cv2.imshow("cam",frame)
    cv2.waitKey(10)
}

while(1==1):
    detect()