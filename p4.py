import cv2

#Görüntünün boyutu (480, 640, 3) (yükseklik, genişlik, renk kanalı)

cap = cv2.VideoCapture(0)

success, img = cap.read()

print(img.shape)