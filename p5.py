import cv2

#real-time processing pipeline

cap = cv2.VideoCapture(0)

while True:

    success, img = cap.read()

    cv2.imshow("Camera", img)

    print(img.shape)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()