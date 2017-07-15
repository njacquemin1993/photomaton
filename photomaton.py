#!/usr/bin/env python

import cv2
import time
import datetime
import numpy as np
from PIL import Image

NOT_SELECTED = 0
SELECTED = 1

background = Image.open("background.png")

def blend_transparent(face_img, overlay_t_img):
    face = Image.frombytes("RGB", (1920, 1080), face_img.tostring())
    face.paste(overlay_t_img, (0,0), overlay_t_img)
    return np.array(face)

def update_video(window_name, cam):
    ret, frame = cam.read()
    #vertical flip image
    frame = cv2.flip(frame, 1)
    frame = blend_transparent(frame, background)
    cv2.imshow(window_name, frame)
    key = cv2.waitKey(1) % 0x100
    return frame, key

def write_text(frame, text, position, selected):
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontsize = 2
    color = (255,255,255)
    thickness = 4
    size, _ = cv2.getTextSize(text, font, fontsize, thickness)
    ellipse = (int(size[0]*0.6), int(size[1]*1.1))
    cv2.ellipse(frame, position, ellipse, 0, 0, 360, (50,50,50), -1)
    if selected == SELECTED:
        cv2.ellipse(frame, position, ellipse, 0, 0, 360, (0,255,0), 3)
    x = position[0] - size[0]/2
    y = position[1] + size[1]/2
    cv2.putText(frame, text, (x, y), font, fontsize ,color ,thickness)

def capture_image(window_name, cam, original):
    cont = True
    choice = 1
    while cont:
        frame = original.copy()
        if choice == 2:
            write_text(frame, "Enregistrer", (1920/2-200, 1000), NOT_SELECTED)
            write_text(frame, "Annuler", (1920/2+200, 1000), SELECTED)
        elif choice == 1:
            write_text(frame, "Enregistrer", (1920/2-200, 1000), SELECTED)
            write_text(frame, "Annuler", (1920/2+200, 1000), NOT_SELECTED)
        cv2.imshow(window_name, frame)
        key = None
        while key not in [ord("a"), ord("d"), ord("s")]:
            key = cv2.waitKey(1) % 0x100
        if key == ord("a"): #left
            choice = 1
        elif key == ord("d"): #right
            choice = 2
        elif key == ord("s"): #enter
            if choice == 1:
                name = datetime.datetime.now().strftime("%Y-%m-%d-%H%M") + ".png"
                cv2.imwrite(name, original)
            cont = False

def main(window_name="photomaton"):
    cam = cv2.VideoCapture(1)
    cam.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 1920)
    cam.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 1080)
    cam.set(cv2.cv.CV_CAP_PROP_FPS, 60)
    cam.set(cv2.cv.CV_CAP_PROP_BRIGHTNESS, 0.5)
    cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.cv.CV_WINDOW_FULLSCREEN)
    while True:
        frame, key = update_video(window_name, cam)
        if key == ord('q'):
            cam.release()
            cv2.destroyAllWindows()
            exit()
        elif key == ord(' '):
            capture_image(window_name, cam, frame)

if __name__ == "__main__":
    main()
