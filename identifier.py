import cv2
import numpy
from datetime import datetime
from threading import Timer, Thread, Event
from state_machine_builders import DracozoltStateMachineBuilder
import time

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

class ThreadsInUse():
  def __init__(self):
    self.player_hint = False
    self.menu_selection_arrow = False
    self.dialog_arrow = False
    self.r_to_boxes = False
    self.box_arrow = False
    self.shiny_marker = False
    self.dialog_next = False
    self.dialog_next_inverted = False
    self.change_user_hint = False
    self.close_app_hint = False

##----- globals
current_frame = None
locations = Locations()
threads_in_use = ThreadsInUse()
join_threads = False

##----- templates
def mount_rect(h,w):
  def _mount_rect(pt):
    return (pt, (pt[0] + w, pt[1] + h))
  return _mount_rect

def finder_factory(name, threshold, all):
  def _find_internals(synchronization_event):
    global current_frame, locations, join_threads

    template = cv2.imread(f"./templates/{name}.jpg")

    while True:
      if join_threads:
        return

      synchronization_event.wait()
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

  return _find_internals

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
show_frame = True
fps = 4

if show_frame:
  cv2.namedWindow('frame')

# Threads
threads = {}
for data in input_data:
  synchronization_event = Event()
  thread = Thread(target=finder_factory(data[0], data[1], data[2]), args=(synchronization_event,))
  thread.start()
  threads[data[0]]={"thread": thread, "event": synchronization_event}

# State Machine
state_machine = DracozoltStateMachineBuilder(locations, threads_in_use).build()

# Main Loop
while True:
  loop_start_time = datetime.now()
  ret, frame = video.read()

  for thread_name in threads_in_use.__dict__:
    if not threads_in_use.__dict__[thread_name]:
      locations.__dict__[f"{thread_name}_location"] = None
      continue
    else:
      threads[thread_name]["event"].set()
      
  current_frame = frame

  for thread_name in threads:
    threads[thread_name]["event"].clear()

  shown_frame = None
  if show_frame:
    shown_frame = frame

  if show_frame and draw_boxes:
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

  if show_frame:
    cv2.imshow('frame', shown_frame)
  
    pressed_key = cv2.waitKey(1) & 0xFF

    if pressed_key == ord('q'):
      break
  
  state_machine.step()
  
  loop_end_time = datetime.now()
  loop_time_diff = (loop_end_time - loop_start_time).total_seconds()
  time.sleep(max((1/fps)-loop_time_diff, 0))

join_threads = True
for thread_name in threads:
  threads[thread_name]["event"].set()
  threads[thread_name]["thread"].join()

video.release()
cv2.destroyAllWindows()