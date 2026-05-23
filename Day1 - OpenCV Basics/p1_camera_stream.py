import cv2 #OpenCV kütüphanesi

cap = cv2.VideoCapture(0) #bilgisayar kamerası açılıyor. cap:video capture object
                          
while True:
    success, img = cap.read() #kameradan yeni frame alır

    cv2.imshow("Camera", img) #Görüntüyü Gösterme

    if cv2.waitKey(1) & 0xFF == ord('q'): #klavyeden input bekler
        break

cap.release() #Kamera Kaynağını Serbest Bırakma
cv2.destroyAllWindows() 