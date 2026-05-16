#HUD System Example

import cv2
import time

cap = cv2.VideoCapture(0)

prev_time = 0

while True:

    success, img = cap.read()

    # Görüntüyü aynala
    img = cv2.flip(img, 1)

    # Kamera çerçevesi
    cv2.rectangle(img, (15,15), (620,460), (0,255,0), 2)

    # Center crosshair:hedef işareti
    cv2.line(img, (320,200), (320,280), (0,255,0), 2)
    cv2.line(img, (280,240), (360,240), (0,255,0), 2)

    # Target circle
    cv2.circle(img, (320,240), 40, (255,0,255), 2)

    # Başlık
    cv2.putText(
        img,
        "CV CAMERA HUD",
        (350,50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255,255,0),
        2
    )

    # Recording yazısı
    cv2.putText(
        img,
        "REC",
        (535,90),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0,0,255),
        2
    )

    # Recording ışığı
    cv2.circle(img, (610,80), 10, (0,0,255), -1)

    cv2.imshow("HUD System", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()