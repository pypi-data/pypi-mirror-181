import cv2
import numpy as np

def capturePaper(ok_key = 'a'):
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    while cv2.waitKey(33) & 0xFF != ord(ok_key):
        ret, frame = cap.read()
        image = frame.copy()
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        ret, threshold = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 400: 
                approx = cv2.approxPolyDP(cnt, 0.009 * cv2.arcLength(cnt, True), True)
                if(len(approx) == 4): 
                    cv2.drawContours(frame, [approx], 0, (1, 194, 252), 4)
                    break
        cv2.imshow("frame", frame)

    cap.release()
    cv2.destroyAllWindows()

    (x, y, w, h) = cv2.boundingRect(approx)
    if w > h:
        w = round(h * 1.414)
    else:
        h = round(w * 1.414)
    src = np.array([a[0] for a in approx], dtype=np.float32)
    dst = np.array([[0, 0], [0, h], [w, h], [w, 0]], dtype=np.float32)

    matrix = cv2.getPerspectiveTransform(src, dst)
    warped = cv2.warpPerspective(image, matrix, (w, h))
    return warped

if __name__ == '__main__':
    res = capturePaper()
    cv2.imshow("result", res)
    cv2.waitKey()
    cv2.destroyAllWindows()
