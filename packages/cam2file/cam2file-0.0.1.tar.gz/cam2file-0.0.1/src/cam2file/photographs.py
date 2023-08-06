from . import core
import cv2

def handle_image(a):
    img = core.capturePaper()
    cv2.imwrite(a,img)
