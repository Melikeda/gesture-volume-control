import cv2
import mediapipe as mp

# MediaPipe Hands
mp_hands = mp.solutions.hands

# Hands nesnesi
hands = mp_hands.Hands()

# Kamera
cap = cv2.VideoCapture(0)

while True:

    success, img = cap.read()

    img = cv2.flip(img, 1)

    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb_img)

    # Eğer el varsa
    if results.multi_hand_landmarks:

        # Her el için: çünkü birden fazla el olabilir
        for handLms in results.multi_hand_landmarks: 

            # 21 noktayı dolaş
            for id, lm in enumerate(handLms.landmark):

                print(id, lm)

    cv2.imshow("Hand Tracking", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()