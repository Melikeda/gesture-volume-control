import cv2
import time

cap = cv2.VideoCapture(0)

prev_time = 0

while True:

    success, img = cap.read()

    img = cv2.flip(img, 1)

    #tuple unpacking:
    h, w, c = img.shape

    center_x = w // 2
    center_y = h // 2

    # FPS hesaplama
    current_time = time.time()

    fps = 1 / (current_time - prev_time)

    prev_time = current_time

    # OUTER FRAME

    cv2.rectangle(img, (20,20), (620,460), (255,255,0), 2)

    # CORNER LINES

    # Sol üst
    cv2.line(img, (20,20), (80,20), (0,25,0), 3)
    cv2.line(img, (20,20), (20,80), (25,255,0), 3)

    # Sağ üst
    cv2.line(img, (620,20), (560,20), (0,25,0), 3)
    cv2.line(img, (620,20), (620,80), (25,255,0), 3)

    # Sol alt
    cv2.line(img, (20,460), (80,460), (0,25,0), 3)
    cv2.line(img, (20,460), (20,400), (25,255,0), 3)

    # Sağ alt
    cv2.line(img, (620,460), (560,460), (0,25,0), 3)
    cv2.line(img, (620,460), (620,400), (25,255,0), 3)

    # CENTER TARGET

    cv2.circle(img, (center_x, center_y), 100, (0,255,255), 2)

    cv2.circle(img, (center_x, center_y), 10, (0,0,255), -1)

    # Crosshair
    cv2.line(img, (center_x-50, center_y),
             (center_x+50, center_y), (0,255,255), 2)

    cv2.line(img, (center_x, center_y-50),
             (center_x, center_y+50), (0,255,255), 2)

    # TEXTS

    cv2.putText(
        img,
        "JARVIS SYSTEM",
        (20,50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0,255,255),
        2
    )

    cv2.putText(
        img,
        f"FPS: {int(fps)}",
        (20,90),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0,255,0),
        2
    )

    cv2.putText(
        img,
        "TARGET LOCK",
        (220,120),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0,0,255),
        2
    )

    # SCAN LINES

    cv2.line(img, (0, center_y),
             (w, center_y), (255,0,255), 1)

    cv2.imshow("IRON MAN HUD", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()