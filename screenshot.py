import cv2
import numpy
from datetime import datetime

dt = datetime.now()
ts = datetime.timestamp(dt)

video = cv2.VideoCapture(0)

shot_count = 0

cv2.namedWindow('frame')

while True:
  ret, frame = video.read()

  cv2.imshow('frame', frame)
  
  pressed_key = cv2.waitKey(1) & 0xFF

  if pressed_key == ord('q'):
    break
  if pressed_key == ord('s'):
    cv2.imwrite(f'./shots/{ts}_{shot_count}.jpg', frame)
    shot_count += 1

video.release()
cv2.destroyAllWindows()