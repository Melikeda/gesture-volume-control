import cv2

cap = cv2.VideoCapture(0)

while True:

    success, img = cap.read()

    # Görüntüyü aynala
    img = cv2.flip(img, 1)

    # Çizgi
    cv2.line(img, (0,0), (640,480), (100,200,300), 5)

    # Rectangle
    cv2.rectangle(img, (150,100), (500,350), (0,255,0), 5)

    # Circle
    cv2.circle(img, (320,240), 100, (123,45,200), -5)

    # Yazı
    cv2.putText(
        img,                         #görüntü,
        "Hello OpenCV",              #yazı,
        (200,100),                   #konum,
        cv2.FONT_HERSHEY_TRIPLEX,    #font,
        1,                           #boyut,
        (137,0,25),                  #renk,
        2                            #kalınlık
    )

    cv2.imshow("Camera", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()