#!/usr/bin/env python

import glob
import os
import cv2
import numpy as np
import time
from PIL import Image

TIME = 5

def write_text(frame, text, position):
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontsize = 2
    color = (255,255, 255)
    thickness = 4
    size, _ = cv2.getTextSize(text, font, fontsize, thickness)
    x = position[0] - size[0]/2
    y = position[1] + size[1]/2
    cv2.rectangle(frame, (x-10, y+10), (x+size[0]+10, y-size[1]-10), (0, 0, 0), -1) 
    cv2.putText(frame, text, (x, y), font, fontsize ,color ,thickness)

def main(window_name="viewer"):
    cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.cv.CV_WINDOW_FULLSCREEN)
    while True:
        for image_path in sorted(glob.glob("Photos/*.png")):
            time.sleep(0.2)
            try:
                image = cv2.cvtColor(np.array(Image.open(image_path)), cv2.COLOR_RGB2BGR)
            except cv2.error:
                image = cv2.cvtColor(np.array(Image.open(image_path)), cv2.COLOR_GRAY2BGR)
            write_text(image, os.path.basename(image_path)[:-4], (1920/2, 1000))
            cv2.imshow(window_name, image)
            count = TIME * 1000
            while count > 0:
                key = cv2.waitKey(1) % 0x100
                if key == ord('q'):
                    cv2.destroyAllWindows()
                    exit()
                count -= 1

if __name__ == "__main__":
    main()
