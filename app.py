'''import numpy as np
import cv2
from PIL import ImageGrab

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter("out.mp4", fourcc, 5.0, (1200, 750))

while(True):
    screen = np.array(ImageGrab.grab(bbox=(0, 40, 800, 640))) #x, y, w, h

    cv2.imshow('Screen',cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
    out.write(screen)

    key = cv2.waitKey(1)
    if key == 27:
        break

out.release()
cv2.destroyAllWindows()'''


# import time
# import cv2
# import mss
# import numpy as np
# import matplotlib as plt
#
# fourcc = cv2.VideoWriter_fourcc(*'XVID')
# out = cv2.VideoWriter("output.avi", fourcc, 20.0,(1280, 720))
# images = []
#
# with mss.mss() as sct:
#     # Part of the screen to capture
#     monitor = {'top': 40, 'left': 0, 'width': 800, 'height': 640}
#
#     while 'Screen capturing':
#         last_time = time.time()
#
#         # Get raw pixels from the screen, save it to a Numpy array
#         img = np.array(sct.grab(monitor))
#         img = cv2.resize(img, (1280, 720))
#         frame = img
#
#         cv2.putText(frame, "FPS: %f" % (1.0 / (time.time() - last_time)),
#                     (10, 10),  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
#         out.write(frame)
#         cv2.imshow('frame', frame)
#
#         images.append(frame)
#
#         print('fps: {0}'.format(1 / (time.time()-last_time)))
#
#         # Press "q" to quit
#         if cv2.waitKey(25) & 0xFF == ord('q'):
#             #for i in range(len(images)):
#                 #out.write(images[i])
#             out.release()
#             cv2.destroyAllWindows()
#             break

'''
import sys
import time
import numpy

from screen_recorder_sdk import screen_recorder


def main ():
    screen_recorder.enable_dev_log ()
    pid = sys.argv[1]
    screen_recorder.init_resources (pid)

    screen_recorder.get_screenshot (5).save ('test_before.png')

    screen_recorder.start_video_recording ('video1.mp4', 30, 8000000, True)
    time.sleep (5)
    screen_recorder.get_screenshot (5).save ('test_during_video.png')
    time.sleep (5)
    screen_recorder.stop_video_recording ()

    screen_recorder.start_video_recording ('video2.mp4', 30, 8000000, True)
    time.sleep (5)
    screen_recorder.stop_video_recording ()

    screen_recorder.free_resources ()

if __name__ == "__main__":
    main ()
'''
import cv2

cap = cv2.VideoCapture(0)

while(True):
    ret, frame = cap.read()
    cv2.imshow("ghen co vy",frame)
    if cv2.waitKey(10) & 0xff == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
