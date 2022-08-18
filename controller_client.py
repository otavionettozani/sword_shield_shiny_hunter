import requests 

class ControllerClient:
  def __init__(self, base_url="http://192.168.0.151:5000", mock=False):
    self.base_url = base_url
    self.mock = mock

  def _press_button(self, button):
    if self.mock:
      print(f"short press {button}")
      return

    try:
      body = {"buttons": [button], "time": 0.05}
      requests.post(f"{self.base_url}/api/v1/press",json=body)
    except:
      print("Error")
      exit()

  def _long_press_button(self, button):
    if self.mock:
      print(f"long press {button}")
      return

    try:
      body = {"buttons": [button], "time": 2}
      requests.post(f"{self.base_url}/api/v1/press",json=body)
    except:
      print("Error")
      exit()
  
  def press_A(self):
    self._press_button("A")
  
  def press_Up(self):
    self._press_button("Up")

  def press_Down(self):
    self._press_button("Down")

  def press_Left(self):
    self._press_button("Left")

  def press_Right(self):
    self._press_button("Right")
  
  def press_X(self):
    self._press_button("X")

  def press_home(self):
    self._press_button("home")

  def press_R(self):
    self._press_button("R")

  def press_Y(self):
    self._press_button("Y")

  def capture(self):
    self._long_press_button("capture")