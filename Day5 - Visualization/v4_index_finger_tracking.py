import cv2
import mediapipe as mp

# MediaPipe Hands
mp_hands = mp.solutions.hands

# Drawing utils
mp_draw = mp.solutions.drawing_utils

# Hands nesnesi
hands = mp_hands.Hands(
    max_num_hands=2
)

# Kamera
cap = cv2.VideoCapture(0)

while True:

    success, img = cap.read()

    img = cv2.flip(img, 1)

    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb_img)

    h, w, c = img.shape

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

                # Sadece işaret parmağı ucu
                if id == 8:

                    # Küçük modern circle
                    cv2.circle(
                        img,
                        (cx, cy),
                        12,
                        (190,0,0),
                        -1
                    )

                    # Yazı
                    cv2.putText(
                        img,
                        "INDEX",
                        (cx - 25, cy - 25),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (0,255,0),
                        2
                    )

    cv2.imshow("Finger Tip Tracking", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()