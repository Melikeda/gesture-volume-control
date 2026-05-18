import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    max_num_hands=2
)

cap = cv2.VideoCapture(0)

while True:

    success, img = cap.read()

    img = cv2.flip(img, 1)

    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb_img)

    h, w, c = img.shape

    # El varsa
    if results.multi_hand_landmarks:

        # Sağ/Sol el bilgisi
        for handNo, handLms in enumerate(results.multi_hand_landmarks):

            # Sağ mı Sol mu
            handType = results.multi_handedness[handNo].classification[0].label

            print("EL:", handType)

            # Landmarkları dolaş
            for id, lm in enumerate(handLms.landmark):

                cx = int(lm.x * w)
                cy = int(lm.y * h)

                print(id, cx, cy)

                # İşaret parmağı ucu
                if id == 8:

                    cv2.circle(
                        img,
                        (cx, cy),
                        15,
                        (255,0,255),
                        -1
                    )

    cv2.imshow("Hand Tracking", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()