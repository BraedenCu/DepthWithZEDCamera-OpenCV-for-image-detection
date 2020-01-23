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

    # Set configuration parameters for ZED stuff
    prefix_point_cloud = "Cloud_"
    prefix_depth = "Depth_"
    path = "./"
    init_params = sl.InitParameters()
    init_params.depth_mode = sl.DEPTH_MODE.DEPTH_MODE_ULTRA # Use ULTRA depth mode
    init_params.coordinate_units = sl.UNIT.UNIT_MILLIMETER # Use millimeter units (for depth measurements)

    # Create an RGBA sl::Mat object
    sl::Mat image_zed(zed.getResolution(), MAT_TYPE_8U_C4);
    # Create an OpenCV Mat that shares sl::Mat data
    cv::Mat image_ocv = slMat2cvMat(image_zed);

    # Create a sl::Mat with float type (32-bit)
    sl::Mat depth_zed(zed.getResolution(), MAT_TYPE_32F_C1);
    # Create an OpenCV Mat that shares sl::Mat data
    cv::Mat depth_ocv = slMat2cvMat(depth_zed);

    if zed.grab() == SUCCESS :
        # Retrieve the left image in sl.Mat
        zed.retrieve_image(image_zed, sl.VIEW.VIEW_LEFT)
        # Use get_data() to get the numpy array
        image_ocv = image_zed.get_data()
        # Display the left image from the numpy array
        cv2.imshow("Image", image_ocv)
        # Retrieve the depth measure (32-bit)
        zed.retrieveMeasure(depth_zed, MEASURE_DEPTH);
        # Print the depth value at the center of the image
        std::cout << depth_ocv.at<float>(depth_ocv.rows/2, depth_ocv.cols/2) << std::endl;
    
    depth_value = depth_map.get_value(x,y)

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
    
    