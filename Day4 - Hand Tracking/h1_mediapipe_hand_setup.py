import cv2
import mediapipe as mp  

# MediaPipe Hands
mp_hands = mp.solutions.hands

# Hands nesnesi oluştur
hands = mp_hands.Hands()

# Kamera
cap = cv2.VideoCapture(0)

while True:

    success, img = cap.read()

    # Aynalama
    img = cv2.flip(img, 1)

    # BGR -> RGB
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  #MediaPipe RGB ister.

    # Eli işle
    results = hands.process(rgb_img)

    # Sonucu yazdır
    print(results.multi_hand_landmarks)

    # Kamerayı göster
    cv2.imshow("Hand Tracking", img)

    # q ile çık
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()