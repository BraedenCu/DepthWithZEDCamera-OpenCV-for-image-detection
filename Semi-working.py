import pyzed.sl as sl
import math
import numpy as np
import sys
import cv2

print("o")

def main():
    print("started setup")
    lowerBound=np.array([33,80,40])
    upperBound=np.array([102,255,255])
    red = (255,0,0)
    distance = 1
    xcenter = 1
    center = 0
    cam = cv2.VideoCapture(1)

    kernelOpen=np.ones((5,5))
    kernelClose=np.ones((20,20))
        
# Create a Camera object
    zed = sl.Camera()

    # Create a InitParameters object and set configuration parameters
    init_params = sl.InitParameters()
    init_params.depth_mode = sl.DEPTH_MODE.DEPTH_MODE_PERFORMANCE  # Use PERFORMANCE depth mode
    init_params.coordinate_units = sl.UNIT.UNIT_MILLIMETER  # Use milliliter units (for depth measurements)

    # Open the camera
    err = zed.open(init_params)
    #if err != sl.ERROR_CODE.SUCCESS:
        #exit(1)

    # Create and set RuntimeParameters after opening the camera
    runtime_parameters = sl.RuntimeParameters()
    runtime_parameters.sensing_mode = sl.SENSING_MODE.SENSING_MODE_STANDARD  # Use STANDARD sensing mode

    # Capture 50 images and depth, then stop
    i = 0
    image = sl.Mat()
    depth = sl.Mat()
    point_cloud = sl.Mat()

    print("ran setup")

    while i < 100:

        #OPENCV CODE
        print("ran start of opencv")
        ret, image = cam.read()
        ret, img = cam.read()
        frame = cv2.resize(image, (250, 250))
        imgHSV = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
       
        mask=cv2.inRange(imgHSV,lowerBound,upperBound)
        
        maskOpen=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernelOpen)
        maskClose=cv2.morphologyEx(maskOpen,cv2.MORPH_CLOSE,kernelClose)

        maskFinal=maskClose
        _, conts, _= cv2.findContours(maskFinal.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for i in range(len(conts)):
       
            c =  max(conts,key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            if radius > 50:
                x,y,w,h=cv2.boundingRect(conts[i])
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255), 2)
                print(center)
                xcenter = (int(M["m10"] / M["m00"]))
                ycenter = (int(M["m01"] / M["m00"]))
                distance = int(xcenter - 125)
                table.putNumber('x', xcenter)
            else:
                table.putNumber('x', 125)
        #END OF OPENCV CODE
        print("ended opencv")

        # A new image is available if grab() returns SUCCESS
        # A new image is available if grab() returns SUCCESS
        if zed.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:
            # Retrieve left image                                                                                                   zed.retrieve_image(image, sl.VIEW.VIEW_LEFT)
            # Retrieve depth map. Depth is aligned on the left image
            print("ran zed")
            zed.retrieve_measure(depth, sl.MEASURE.MEASURE_DEPTH)
            # Retrieve colored point cloud. Point cloud is aligned on the left image.
            zed.retrieve_measure(point_cloud, sl.MEASURE.MEASURE_XYZRGBA)

            # Get and print distance value in mm at the center of the image
            # We measure the distance camera - object using Euclidean distance
            #x = round(image.get_width() / 2)
            #y = round(image.get_height() / 2)
            x = xcenter
            y = ycenter

            err, point_cloud_value = point_cloud.get_value(x, y)
            distance = math.sqrt(point_cloud_value[0] * point_cloud_value[0] +                                                                           point_cloud_value[1] * point_cloud_value[1] +
                                 point_cloud_value[2] * point_cloud_value[2])

            if not np.isnan(distance) and not np.isinf(distance):
                distance = round(distance)
                print("Distance to Camera at ({0}, {1}): {2} mm\n".format(x, y, distance))
                # Increment the loop
                i = i + 1
            else:
                print("Can't estimate distance at this position, move the camera\n")
            sys.stdout.flush()

    # Close the camera                                                                                                      zed.close()                                                                                                         
    zed.close()

if __name__ == "__main__":
    main()
