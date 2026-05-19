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

    # El varsa
    if results.multi_hand_landmarks:

        for handLms in results.multi_hand_landmarks:

            # Özelleştirilmiş çizim
            mp_draw.draw_landmarks(
                img,
                handLms,
                mp_hands.HAND_CONNECTIONS,

                # Landmark style
                mp_draw.DrawingSpec(
                    color=(255,0,25), #rengini
                    thickness=2,       #kalınlığını
                    circle_radius=4    #boyutunu
                ),

                # Connection style
                mp_draw.DrawingSpec(
                    color=(0,255,0),
                    thickness=2
                )
            )

    cv2.imshow("Hand Visualization", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()