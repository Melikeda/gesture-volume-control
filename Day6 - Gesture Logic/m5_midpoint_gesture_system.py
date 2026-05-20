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

            # İki nokta arasına çizgi çiz
            cv2.line(
                img,
                (thumb_x, thumb_y),
                (index_x, index_y),
                (255,255,255),
                3
            )

            # Mesafe hesabı
            distance = math.hypot(
                index_x - thumb_x,
                index_y - thumb_y
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

            # Orta nokta hesabı
            mid_x = int((thumb_x + index_x) / 2)
            mid_y = int((thumb_y + index_y) / 2)

            # Orta noktaya circle çiz
            cv2.circle(
                img,
                (mid_x, mid_y),
                10,
                (255,255,0),
                -1
            )

            # Parmaklar yakın mı?
            if distance < 50:

                # Kırmızı circle
                cv2.circle(
                    img,
                    (320,240),
                    40,
                    (0,0,255),
                    -1
                )

                cv2.putText(
                    img,
                    "CLOSE",
                    (250,100),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0,0,255),
                    3
                )

            # Parmaklar uzak mı?
            else:

                # Yeşil circle
                cv2.circle(
                    img,
                    (320,240),
                    40,
                    (0,255,0),
                    -1
                )

                cv2.putText(
                    img,
                    "OPEN",
                    (260,100),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0,255,0),
                    3
                )

    cv2.imshow("Gesture Feedback System", img)

    # q ile çık
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()