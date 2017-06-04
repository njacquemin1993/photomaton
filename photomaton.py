#!/usr/bin/env python

import cv2
import time

def update_video(window_name, cam):
	ret, frame = cam.read()
	cv2.imshow(window_name, frame)
	key = cv2.waitKey(10) 
	return key % 0x100 != ord('q')

def main(window_name="photomaton"):
	cam = cv2.VideoCapture(0)
	cam.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 1920)
	cam.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 1080)
	cam.set(cv2.cv.CV_CAP_PROP_FPS, 60)
	cam.set(cv2.cv.CV_CAP_PROP_BRIGHTNESS, 0.5)
	cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)          
        cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.cv.CV_WINDOW_FULLSCREEN)
	while update_video(window_name, cam):
		pass
	cv2.destroyAllWindows()
	cam.release()

if __name__ == "__main__":
	main()
