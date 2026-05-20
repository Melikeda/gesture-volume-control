import cv2
import mediapipe as mp
import math
import numpy as np
from collections import deque

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

# Distance geçmişi
distance_history = deque(maxlen=5)

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

                # Thumb Tip
                if id == 4:

                    thumb_x, thumb_y = cx, cy

                    cv2.circle(
                        img,
                        (thumb_x, thumb_y),
                        15,
                        (0,255,0),
                        -1
                    )

                # Index Tip
                if id == 8:

                    index_x, index_y = cx, cy

                    cv2.circle(
                        img,
                        (index_x, index_y),
                        15,
                        (255,0,255),
                        -1
                    )

            # Distance hesabı
            distance = math.hypot(
                index_x - thumb_x,
                index_y - thumb_y
            )

            # Distance geçmişine ekle
            distance_history.append(distance)

            # Smooth distance
            smooth_distance = np.mean(distance_history)

            # Min distance güncelle
            if smooth_distance < min_distance:

                min_distance = smooth_distance

            # Max distance güncelle
            if smooth_distance > max_distance:

                max_distance = smooth_distance

            # Distance'a göre çizgi rengi
            if smooth_distance < 100:

                line_color = (0,0,255)

            else:

                line_color = (0,255,0)

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
                f"Distance: {int(smooth_distance)}",
                (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0,255,0),
                3
            )

            # Distance -> Bar değeri
            bar_y = np.interp(
                smooth_distance,
                [min_distance, max_distance],
                [400,150]
            )

            # Distance -> Volume %
            volume_percent = np.interp(
                smooth_distance,
                [min_distance, max_distance],
                [0,100]
            )

            # Volume status
            if volume_percent < 30:

                volume_status = "LOW"
                status_color = (0,0,255)

            elif volume_percent < 70:

                volume_status = "MEDIUM"
                status_color = (0,255,255)

            else:

                volume_status = "HIGH"
                status_color = (0,255,0)

            # Bar outline
            cv2.rectangle(
                img,
                (50,150),
                (85,400),
                (255,255,255),
                3
            )

            # Dynamic bar
            cv2.rectangle(
                img,
                (50, int(bar_y)),
                (85,400),
                (0,255,0),
                -1
            )

            # Volume percentage text
            cv2.putText(
                img,
                f'{int(volume_percent)} %',
                (40, 430),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255,255,255),
                3
            )

            # Volume status text
            cv2.putText(
                img,
                volume_status,
                (20, 470),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                status_color,
                3
            )

    cv2.imshow("Gesture Volume UI System", img)

    # q ile çık
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()