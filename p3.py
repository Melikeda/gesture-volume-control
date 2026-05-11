import cv2

#img type türünü verir
#output: <class 'numpy.ndarray'>

cap = cv2.VideoCapture(0)

success, img = cap.read()

print(type(img))