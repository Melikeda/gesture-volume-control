import cv2
import time

cap = cv2.VideoCapture(0)

prev_time = 0

while True:

    success, img = cap.read()

    img = cv2.flip(img, 1)

    # Şu anki zaman
    current_time = time.time()

    # FPS hesaplama
    fps = 1 / (current_time - prev_time)

    prev_time = current_time    #Prev Time:Önceki frame zamanı

    # FPS yazdır
    cv2.putText(
        img,
        f"FPS: {int(fps)}",     #int(fps):Ondalığı kaldırır
        (20,50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0,255,0),
        2
    )

    cv2.imshow("Camera", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()