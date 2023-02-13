 


import threading
import time 
import cv2 
import os

"""
                Camera
This class controls the camera on a raspberry pi, the class can take photos and video
If you are not going to take videos/photos in a while then you could close the objects with cameraStop, just remember to call cameraStart to start the camera again

videoPath = This is the path that the class will save the video files to, the name of the video is a parameter to the video function, example: "/Desktop/EPICVIDEOS/".  (str)
videoRes = This is the resulution of the video, stored in a tuple value, 480 res example: (640, 480)    (tup)
fps = This is the fps of the video, 30 fps example = 30     (int)
#dateName = This is if you want the name of the video to be the current date and time.


imgPath = This is the path that the class will save the photo files to, the name of the photo is a parameter to the video function
imgScaleXY = This is for the scaling of the photo, stored in a tuple. if you want to zoom win with 50% then example: (2,2). If you dont want scaling then input (1,1)   (tup)
imgFlip = This is if you want to flip the image, there is four options to choose from: 1, 0, -1.    (int)
#dateName = This is if you want the name of the photo to be the current date and time.
"""
class Camera:
    
    def __init__(self, videoPath, imgPath, videoRes, fps, imgScaleXY, imgFlip):

	

        self.videoCaptureIndex = 0
        self.videoPath = videoPath
        self.videoRes = videoRes
        self.fps = fps
        self.record = True
    
        self.imgPath = imgPath
        self.scaleXY = imgScaleXY
        self.flip = imgFlip

        self.camera = cv2.VideoCapture(self.videoCaptureIndex) # OPENS UP THE CAMERA

#               cameraStart
#This function makes the camera object, you dont need to call if you just make the object because it is called in the __int__ funciton.
#It is usefull when you close the objects from the cameraStop function
  

    def cameraStart(self): 
        self.camera = cv2.VideoCapture(self.videoCaptureIndex)
		

#            takePhoto
#This function takes photos and stores it with the name inputted in the function and with the path inputted in the creation of the object
#
#imgName = This is the name of the image you want to make, if there is a image with the same name then it will be overitten. NOTE REMEMBER TO ADD THE FILE NAME. example "image.jpg"     (str)      
    def takePhoto(self, imgName):
	
        success, img = self.camera.read() # READS THE IMAGE FROM THE CAMERA
    
        img = cv2.flip(img, self.flip) # FLIPS THE IMAGE
        img = cv2.resize(img, None, fx=self.scaleXY[0], fy=self.scaleXY[1], interpolation=cv2.INTER_LINEAR) # RESIZES THE IMAGE

        cv2.imwrite(self.imgPath + imgName, img) # SAVES THE IMAGE



#            takeVideo
#This function takes video and stores it with the name inputted in the function and with the path inputted in the creation of the object

#videoName = This is the name of the video you want to make, if there is a video with the same name then it will be overitten. NOTE REMEMBER TO ADD THE FILE NAME. example "vdieo.avi"     (str)
#showVideo = This is if you want the video to show live on the desktop (Bool)
  
    def takeVideo(self, videoName, showVideo=False):

        video = cv2.VideoWriter(self.videoPath + videoName, cv2.VideoWriter_fourcc(*'MJPG'), self.fps, self.videoRes) # STARTS THE VIDEO OBJECT

        self.camera.set(3, self.videoRes[0]) # SETS THE RES OF THE VIDEO
        self.camera.set(4, self.videoRes[1]) # SETS THE RES OF THE VIDEO

        while self.record:
            sucsess, img = self.camera.read() # READS THE PICTURE OF THE CAMERA
    
            if showVideo == True: # IF THE VIDEO SHULD BE SHOWN LIVE ON DESKOP
                cv2.imshow("image", img) # SHOWS THE IMAGE ON DESKTOP


            video.write(img) # WRITES THE IMAGE TO THE VIDEO OBJECT

        self.record = True # RESETS THE RECORD VARIABLE, SO THE ONLY THING YOU NEED TO DO TO START ANOTHER VIDEO IS TO CALL THE FUNCTION
       


#            cameraStop
#This function is usefull if you are not going to be taking photos for a while, it removes the camera object in the class

    def cameraStop(self):
        self.camera.release() # RELEASES THE CAMERA OBJECT
        cv2.destroyAllWindows() # CLOSES ALL OF THE WINDOWS OPENCV OPENED (IF)





#camera = Camera(videoPath="/home/pi/Desktop/Cansat/RaspiCamera/video/", imgPath="/home/pi/Desktop/Cansat/RaspiCamera/img/", videoRes=(640, 480), fps=10, imgScaleXY=(1,1), imgFlip=-1)
#
#
#
#
#i=0
#while True: 
#    i+=1 
#    camera.takePhoto(str(i) + ".jpg")
#    time.sleep(1)





#cameraThread = threading.Thread(target=camera.takeVideo, args=("video.avi", True))
#cameraThread.start()
#time.sleep(2)
#camera.record = False

#camera.cameraStop()

