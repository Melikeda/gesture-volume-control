import cv2

#kameradan tek bir frame alır

cap = cv2.VideoCapture(0)

success, img = cap.read()

cv2.imshow("Image", img)

cv2.waitKey(0)