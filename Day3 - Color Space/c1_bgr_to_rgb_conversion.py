import cv2

cap = cv2.VideoCapture(0)

while True:

    success, img = cap.read()

    # Görüntüyü aynala
    img = cv2.flip(img, 1)

    # BGR -> RGB
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  #görüntünün renk uzayını değiştiriyor

    # BGR -> Grayscale
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #Renk bilgisini kaldırıyor

    print(img.shape)

    print(gray_img.shape)

    # Pencereler
    cv2.imshow("Original", img)

    cv2.imshow("RGB", rgb_img)

    cv2.imshow("Gray", gray_img)

    # q ile çık
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()