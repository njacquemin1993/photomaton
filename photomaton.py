#!/usr/bin/env python

import os
import cv2
import numpy as np
from PIL import Image

NOT_SELECTED = 0
SELECTED = 1

background = []
background.append("EMPTY")
background.append("BW")
background.append(Image.open("Filters/Beach.png"))
background.append(Image.open("Filters/Instagram.png"))
background.append(Image.open("Filters/Wedding.png"))
background.append(Image.open("Filters/Movie.png"))

FRAME_NUMBER = len(background)

LEFT_KEY = ord("f")
CENTER_KEY = ord("k")
RIGHT_KEY = ord("$")

count = 1

def blend_transparent(face_img, overlay_t_img):
    face = Image.frombytes("RGB", (1920, 1080), cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB).tostring())
    face.paste(overlay_t_img, (0,0), overlay_t_img)
    return cv2.cvtColor(np.array(face), cv2.COLOR_RGB2BGR)

def update_video(window_name, cam, frame_index):
    ret, frame = cam.read()
    frame = cv2.resize(frame, (1920, 1080))
    #vertical flip image
    frame = cv2.flip(frame, 1)
    if type(background[frame_index]) == str:
        if background[frame_index] == "BW":
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    else:
        frame = blend_transparent(frame, background[frame_index])
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
    global count
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
        while key not in [LEFT_KEY, CENTER_KEY, RIGHT_KEY]:
            key = cv2.waitKey(1) % 0x100
        if key == LEFT_KEY:
            choice = 1
        elif key == RIGHT_KEY:
            choice = 2
        elif key == CENTER_KEY:
            if choice == 1:
                name = os.path.join("Photos", "{:04d}.png".format(count))
		while os.path.exists(name):
                    count += 1
                    name = os.path.join("Photos", "{:04d}.png".format(count))
                cv2.imwrite(name, original)
                thumb = cv2.resize(original, (384, 216)) 
                cv2.imwrite(os.path.join("Photos/mini", "{:04d}.png".format(count)), thumb)
            cont = False

def main(window_name="photomaton"):
    cam = cv2.VideoCapture(1)
    cam.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 1920)
    cam.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 1080)
    cam.set(cv2.cv.CV_CAP_PROP_FPS, 30)
    cam.set(cv2.cv.CV_CAP_PROP_BRIGHTNESS, 0.5)
    cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.cv.CV_WINDOW_FULLSCREEN)
    frame_index = 0
    while True:
        frame, key = update_video(window_name, cam, frame_index)
        if key == ord('q'):
            cam.release()
            cv2.destroyAllWindows()
            exit()
        elif key == CENTER_KEY:
            capture_image(window_name, cam, frame)
        elif key == RIGHT_KEY:
            frame_index = (frame_index + 1) % FRAME_NUMBER
        elif key == LEFT_KEY:
            frame_index = (frame_index - 1) % FRAME_NUMBER

if __name__ == "__main__":
    main()
