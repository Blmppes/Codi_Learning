import pyscreenshot as ImageGrab
import numpy as np
import cv2

cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
vid = cv2.VideoWriter('output2.mp4', fourcc, 6, (640,480))

while(True):
    img = ImageGrab.grab() #bbox specifies specific region (bbox= x,y,width,height)
    img_np = np.array(img)
    cv2.imshow("test", img_np)
    cv2.imwrite("img.png",img_np)
    if cv2.waitKey(1) == 27:
        break

vid.release()
cv2.destroyAllWindows()
