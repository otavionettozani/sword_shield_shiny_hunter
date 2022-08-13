import cv2
import numpy
from datetime import datetime

dt = datetime.now()
ts = datetime.timestamp(dt)

video = cv2.VideoCapture(1)

initial_point = (100, 100)
final_point = (0,0)
is_drawing = False
crop_count = 0

def mouse_event(event, x, y, flags, params):
  global is_drawing, initial_point, final_point
  if event == cv2.EVENT_LBUTTONDOWN:
    is_drawing = True
    initial_point = (x,y)
    final_point = (x,y)
  elif event == cv2.EVENT_MOUSEMOVE:
    if is_drawing:
      final_point = (x,y)
  elif event == cv2.EVENT_LBUTTONUP:
    is_drawing = False

cv2.namedWindow('frame')
cv2.setMouseCallback('frame', mouse_event)

while True:
  ret, frame = video.read()

  updated_frame = cv2.rectangle(frame, initial_point, final_point, (255, 255, 255), 3)

  cv2.imshow('frame', updated_frame)
  
  pressed_key = cv2.waitKey(1) & 0xFF

  if pressed_key == ord('q'):
    break
  if pressed_key == ord('s'):
    initial_x = min(initial_point[1], final_point[1])+3
    initial_y = min(initial_point[0], final_point[0])+3
    final_x = max(initial_point[1], final_point[1])-3
    final_y = max(initial_point[0], final_point[0])-3
    frame_piece = frame[initial_x:final_x, initial_y:final_y]
    cv2.imshow('cropped', frame_piece)
    cv2.imwrite(f'./cropped/{ts}_{crop_count}.jpg', frame_piece)
    crop_count += 1

video.release()
cv2.destroyAllWindows()