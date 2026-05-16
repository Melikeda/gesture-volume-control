import cv2

cap = cv2.VideoCapture(0)

while True:

    success, img = cap.read()

    img = cv2.flip(img, 1)


    #cv2.line(img, başlangıç, bitiş, renk, kalınlık)
    cv2.line(img, (160,120), (480,120), (255,0,0), 5)

    cv2.line(img, (160,120), (160,360), (0,0,255), 5)

    cv2.line(img, (480,120), (480,360), (0,255,255), 5)

    cv2.line(img, (160,360), (480,360), (255,0,255), 5)

    cv2.imshow("Camera", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

