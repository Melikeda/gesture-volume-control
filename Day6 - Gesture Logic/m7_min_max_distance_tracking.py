import cv2
import mediapipe as mp
import math

# MediaPipe Hands
mp_hands = mp.solutions.hands

# Drawing utils
mp_draw = mp.solutions.drawing_utils

# Hands nesnesi
hands = mp_hands.Hands(
    max_num_hands=1
)

# Kamera
cap = cv2.VideoCapture(0)

# Min-Max distance
min_distance = 1000
max_distance = 0

while True:

    success, img = cap.read()

    # Aynalama
    img = cv2.flip(img, 1)

    # BGR -> RGB
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Hand tracking
    results = hands.process(rgb_img)

    # Görüntü boyutu
    h, w, c = img.shape

    # Thumb koordinatları
    thumb_x, thumb_y = 0, 0

    # Index koordinatları
    index_x, index_y = 0, 0

    # El varsa
    if results.multi_hand_landmarks:

        for handLms in results.multi_hand_landmarks:

            # Hand skeleton çiz
            mp_draw.draw_landmarks(
                img,
                handLms,
                mp_hands.HAND_CONNECTIONS
            )

            # Landmarkları dolaş
            for id, lm in enumerate(handLms.landmark):

                # Normalize -> Pixel
                cx = int(lm.x * w)
                cy = int(lm.y * h)

                # Thumb Tip → LM4
                if id == 4:

                    thumb_x, thumb_y = cx, cy

                    cv2.circle(
                        img,
                        (thumb_x, thumb_y),
                        15,
                        (0,255,0),
                        -1
                    )

                # Index Tip → LM8
                if id == 8:

                    index_x, index_y = cx, cy

                    cv2.circle(
                        img,
                        (index_x, index_y),
                        15,
                        (255,0,255),
                        -1
                    )

            # Mesafe hesabı
            distance = math.hypot(
                index_x - thumb_x,
                index_y - thumb_y
            )

            # Min distance güncelle
            if distance < min_distance:

                min_distance = distance

            # Max distance güncelle
            if distance > max_distance:

                max_distance = distance

            # Distance'a göre çizgi rengi
            if distance < 100:

                line_color = (0,0,255)
                status_text = "CLOSE"
                status_color = (0,0,255)

            else:

                line_color = (0,255,0)
                status_text = "OPEN"
                status_color = (0,255,0)

            # Çizgi çiz
            cv2.line(
                img,
                (thumb_x, thumb_y),
                (index_x, index_y),
                line_color,
                3
            )

            # Distance yazdır
            cv2.putText(
                img,
                f"Distance: {int(distance)}",
                (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0,255,0),
                3
            )

            # Min distance yazdır
            cv2.putText(
                img,
                f"Min: {int(min_distance)}",
                (50,100),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255,255,0),
                2
            )

            # Max distance yazdır
            cv2.putText(
                img,
                f"Max: {int(max_distance)}",
                (50,140),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255,255,0),
                2
            )

            # OPEN / CLOSE yazısı
            cv2.putText(
                img,
                status_text,
                (250,100),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                status_color,
                3
            )

    cv2.imshow("Gesture Range Analysis", img)

    # q ile çık
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()