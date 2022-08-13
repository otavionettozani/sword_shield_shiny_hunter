import cv2
import numpy
from datetime import datetime
from threading import Timer, Thread

class Locations():
  def __init__(self):
    self.player_hint_location = None
    self.menu_selection_arrow_location = None
    self.dialog_arrow_location = None
    self.r_to_boxes_location = None
    self.box_arrow_location = None
    self.shiny_marker_location = None
    self.dialog_next_location = None
    self.dialog_next_inverted_location = None
    self.change_user_hint_location = None
    self.close_app_hint_location = None

##----- globals
current_frame = None
locations = Locations()
join_threads = False

##----- templates
def mount_rect(h,w):
  def _mount_rect(pt):
    return (pt, (pt[0] + w, pt[1] + h))
  return _mount_rect

def finder_factory(name, threshold, all):
  def _find_internals():
    global current_frame, locations, join_threads

    template = cv2.imread(f"./templates/{name}.jpg")

    while True:
      if join_threads:
        return
      if current_frame is None:
        continue
      local_frame = current_frame
      w,h = template.shape[:-1]
      matches = cv2.matchTemplate(local_frame, template, cv2.TM_CCOEFF_NORMED)
      if all:
        filtered_matches = numpy.where(matches >= threshold)
        zipped_matches = list(zip(*filtered_matches[::-1]))
        if len(zipped_matches) > 0:
          pt = zipped_matches[0]
          position = mount_rect(w,h)(pt)
          locations.__dict__[f"{name}_location"] = map(mount_rect(w,h), zipped_matches)
        else:
          locations.__dict__[f"{name}_location"] = None
      else:
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(matches)
        if max_val > threshold:
          position = mount_rect(w,h)(max_loc)
          locations.__dict__[f"{name}_location"] = position
        else:
          locations.__dict__[f"{name}_location"] = None

      # if(name == "shiny_marker"):
      #   print()
      #   print(filtered_matches)
      
      # if len(zipped_matches) > 0:
      #   pt = zipped_matches[0]
      #   position = mount_rect(w,h)(pt)
      #   if all:
      #     locations.__dict__[f"{name}_location"] = map(mount_rect(w,h), zipped_matches)
      #   else:
      #     locations.__dict__[f"{name}_location"] = position
      # else:
      #   locations.__dict__[f"{name}_location"] = None

  return _find_internals


  global current_frame, locations, join_threads

  template = cv2.imread("./templates/box_arrow.jpg")

  while True:
    if join_threads:
      return
    if current_frame is None:
      continue
    local_frame = current_frame
    w,h = template.shape[:-1]
    threshold = .6
    matches = cv2.matchTemplate(local_frame, template, cv2.TM_CCOEFF_NORMED)
    filtered_matches = numpy.where(matches >= threshold)
    zipped_matches = list(zip(*filtered_matches[::-1]))
    if len(zipped_matches) > 0:
      pt = zipped_matches[0]
      position = mount_rect(w,h)(pt)
      # locations.r_to_boxes_location = map(mount_rect(w,h), zipped_matches)
      locations.box_arrow_location = position
    else:
      locations.box_arrow_location = None

## ---- start algorithm

# --- definitions
dt = datetime.now()
video = cv2.VideoCapture(0)
input_data = [
  ("player_hint", 0.8, False, (255, 0, 0)),
  ("menu_selection_arrow", 0.6, False, (0, 255, 0)),
  ("dialog_arrow", 0.5, False, (0, 0, 255)),
  ("r_to_boxes", 0.5, False, (255, 255, 0)),
  ("box_arrow", 0.6, False, (255, 0, 255)),
  ("shiny_marker", 0.6, False, (0, 255, 255)),
  ("dialog_next", 0.7, False, (127, 127, 127)),
  ("dialog_next_inverted", 0.7, False, (255, 255, 255)),
  ("change_user_hint", 0.7, False, (255, 0, 0)),
  ("close_app_hint", 0.7, False, (255, 0, 0))
]
draw_boxes = True

cv2.namedWindow('frame')

# Threads
threads = []
for data in input_data:
  thread = Thread(target=finder_factory(data[0], data[1], data[2]))
  thread.start()
  threads.append(thread)

while True:
  ret, frame = video.read()
  current_frame = frame
  shown_frame = frame
  
  if draw_boxes:
    for data in input_data:
      evaluatable = locations.__dict__[f"{data[0]}_location"]
      if evaluatable != None:
        color = data[3]
        if data[2]:
          found_locations = evaluatable
          for rect_points in found_locations:
            shown_frame = cv2.rectangle(shown_frame, rect_points[0], rect_points[1], color, 2)
        else:
          rect_points = evaluatable
          shown_frame = cv2.rectangle(shown_frame, rect_points[0], rect_points[1], color, 2)

  cv2.imshow('frame', shown_frame)
  
  pressed_key = cv2.waitKey(1) & 0xFF

  if pressed_key == ord('q'):
    break

join_threads = True
for thread in threads:
  thread.join()

video.release()
cv2.destroyAllWindows()