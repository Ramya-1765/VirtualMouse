import cv2
import numpy as np
import pyautogui

pyautogui.FAILSAFE = False

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ Cannot access webcam. Exiting.")
    exit()

screen_w, screen_h = pyautogui.size()

def get_contours(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = np.array([0, 20, 70])
    upper = np.array([20, 255, 255])
    mask = cv2.inRange(hsv, lower, upper)
    mask = cv2.dilate(mask, np.ones((3, 3), np.uint8), iterations=4)
    mask = cv2.GaussianBlur(mask, (5, 5), 100)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours, mask

def get_fingertips(contour):
    hull = cv2.convexHull(contour, returnPoints=False)
    defects = cv2.convexityDefects(contour, hull)
    if defects is None:
        return None, None
    fingertip = None
    thumbtip = None
    points = []
    for i in range(defects.shape[0]):
        s, e, f, _ = defects[i, 0]
        far = tuple(contour[f][0])
        points.append(far)
    if points:
        points = sorted(points, key=lambda p: p[1])
        if len(points) >= 2:
            fingertip, thumbtip = points[0], points[1]
        elif len(points) == 1:
            fingertip = points[0]
    return fingertip, thumbtip

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Failed to read frame from webcam.")
        continue

    frame = cv2.flip(frame, 1)
    frame_h, frame_w, _ = frame.shape

    contours, mask = get_contours(frame)

    if contours:
        contour = max(contours, key=cv2.contourArea)
        if cv2.contourArea(contour) > 3000:
            fingertip, thumbtip = get_fingertips(contour)
            if fingertip:
                x, y = fingertip
                screen_x = np.interp(x, [0, frame_w], [0, screen_w])
                screen_y = np.interp(y, [0, frame_h], [0, screen_h])
                screen_x = max(1, min(screen_x, screen_w - 1))
                screen_y = max(1, min(screen_y, screen_h - 1))

                pyautogui.moveTo(screen_x, screen_y)
                cv2.circle(frame, (x, y), 10, (255, 0, 0), -1)

                if thumbtip:
                    tx, ty = thumbtip
                    distance = np.linalg.norm(np.array([x, y]) - np.array([tx, ty]))
                    if distance < 40:
                        pyautogui.click()
                        cv2.putText(frame, "Click!", (x+20, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("🖱️ AI Virtual Mouse (OpenCV)", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
