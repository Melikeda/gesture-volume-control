import cv2

cap = cv2.VideoCapture(0)

while True:

    success, img = cap.read()

    img = cv2.flip(img, 1)

    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    grayblur_img = cv2.GaussianBlur(gray_img, (15,15), 0)

    blur_img = cv2.GaussianBlur(img, (15,15), 0)

    cv2.imshow("Original", img)

    cv2.imshow("Gray", gray_img)

    cv2.imshow("Blur", blur_img)

    cv2.imshow("GrayBlur", grayblur_img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()