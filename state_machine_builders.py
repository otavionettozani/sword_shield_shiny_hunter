from state_machine import StateMachine, State
from controller_client import ControllerClient

class DracozoltStateMachineBuilder:
  def __init__(self, locations, client=ControllerClient(mock=False)):
    self.locations = locations
    self.client = client

  def build(self):
    def s1_action(state, start_time, current_time):
      button_interval = 3
      if not "last_button_press" in state.data:
        state.data["last_button_press"] = start_time
      interval_since_last_press = (current_time - state.data["last_button_press"]).total_seconds()

      if interval_since_last_press > button_interval:
        self.client.press_A()
        state.data["last_button_press"] = current_time

    def s1_transition(state):
      target_y = 721
      target_x = 1285
      if self.locations.dialog_arrow_location == None:
        return False
      min_box, max_box = self.locations.dialog_arrow_location
      return target_y > min_box[1] and target_y < max_box[1] and target_x > min_box[0] and target_x < max_box[0]

    def s2_action(state, start_time, current_time):
      button_interval = 1
      if not "last_button_press" in state.data:
        state.data["last_button_press"] = start_time
      interval_since_last_press = (current_time - state.data["last_button_press"]).total_seconds()

      if not self.locations.dialog_arrow_location:
        return

      if interval_since_last_press > button_interval:
        target_y = 721
        min_box, max_box = self.locations.dialog_arrow_location
        if target_y > min_box[1] and target_y < max_box[1]:
          self.client.press_A()
          state.data["go_to_next_step"] = True
        elif target_y < min_box[1]:
          self.client.press_Up()
        else:
          self.client.press_Down()
        state.data["last_button_press"] = current_time

    def s2_to_5_transition(state):
      if not "go_to_next_step" in state.data:
        return False
      return state.data["go_to_next_step"] and not self.locations.dialog_arrow_location

    def s3_action(state, start_time, current_time):
      button_interval = 1
      if not "last_button_press" in state.data:
        state.data["last_button_press"] = start_time
      interval_since_last_press = (current_time - state.data["last_button_press"]).total_seconds()

      if not self.locations.dialog_arrow_location:
        return

      if interval_since_last_press > button_interval:
        target_y = 663 # 663 = Bird | 721 = Fish
        min_box, max_box = self.locations.dialog_arrow_location
        if target_y > min_box[1] and target_y < max_box[1]:
          self.client.press_A()
          state.data["go_to_next_step"] = True
        elif target_y < min_box[1]:
          self.client.press_Up()
        else:
          self.client.press_Down()
        state.data["last_button_press"] = current_time

    def s4_action(state, start_time, current_time):
      button_interval = 1
      if not "last_button_press" in state.data:
        state.data["last_button_press"] = start_time
      interval_since_last_press = (current_time - state.data["last_button_press"]).total_seconds()

      if not self.locations.dialog_arrow_location:
        return

      if interval_since_last_press > button_interval:
        target_y = 663 # 663 = Drake | 721 = Dino
        min_box, max_box = self.locations.dialog_arrow_location
        if target_y > min_box[1] and target_y < max_box[1]:
          self.client.press_A()
          state.data["go_to_next_step"] = True
        elif target_y < min_box[1]:
          self.client.press_Up()
        else:
          self.client.press_Down()
        state.data["last_button_press"] = current_time

    def s5_action(state, start_time, current_time):
      button_interval = 1
      if not "last_button_press" in state.data:
        state.data["last_button_press"] = start_time
      interval_since_last_press = (current_time - state.data["last_button_press"]).total_seconds()

      if not self.locations.dialog_arrow_location:
        return

      if interval_since_last_press > button_interval:
        target_y = 663
        min_box, max_box = self.locations.dialog_arrow_location
        if target_y > min_box[1] and target_y < max_box[1]:
          self.client.press_A()
          state.data["go_to_next_step"] = True
        elif target_y < min_box[1]:
          self.client.press_Up()
        else:
          self.client.press_Down()
        state.data["last_button_press"] = current_time

    def s6_to_10_action(state, start_time, current_time):
      button_interval = 1
      if not "last_button_press" in state.data:
        state.data["last_button_press"] = start_time
      interval_since_last_press = (current_time - state.data["last_button_press"]).total_seconds()

      if not self.locations.dialog_next_location:
        return

      if interval_since_last_press > button_interval:
        target_y = 997
        target_x = 1487
        min_box, max_box = self.locations.dialog_next_location
        if target_y > min_box[1] and target_y < max_box[1] and target_x > min_box[0] and target_x < max_box[0]:
          self.client.press_A()
          state.data["go_to_next_step"] = True
        state.data["last_button_press"] = current_time

    def s6_to_10_transition(state):
      if not "go_to_next_step" in state.data:
        return False
      return state.data["go_to_next_step"] and not self.locations.dialog_next_location
        
    def s11_action(state, start_time, current_time):
      button_interval = 1
      if not "last_button_press" in state.data:
        state.data["last_button_press"] = start_time
      interval_since_last_press = (current_time - state.data["last_button_press"]).total_seconds()

      if not self.locations.dialog_next_inverted_location:
        return

      if interval_since_last_press > button_interval:
        target_y = 997
        target_x = 1487
        min_box, max_box = self.locations.dialog_next_inverted_location
        if target_y > min_box[1] and target_y < max_box[1] and target_x > min_box[0] and target_x < max_box[0]:
          self.client.press_A()
          state.data["go_to_next_step"] = True
        state.data["last_button_press"] = current_time

    def s11_12_transition(state):
      if not "go_to_next_step" in state.data:
        return False
      return state.data["go_to_next_step"] and not self.locations.dialog_next_inverted_location

    def s12_action(state, start_time, current_time):
      button_interval = 1
      if not "last_button_press" in state.data:
        state.data["last_button_press"] = start_time
      interval_since_last_press = (current_time - state.data["last_button_press"]).total_seconds()

      if not self.locations.dialog_next_inverted_location:
        return

      if interval_since_last_press > button_interval:
        target_y = 960
        target_x = 1381
        min_box, max_box = self.locations.dialog_next_inverted_location
        if target_y > min_box[1] and target_y < max_box[1] and target_x > min_box[0] and target_x < max_box[0]:
          self.client.press_A()
          state.data["go_to_next_step"] = True
        state.data["last_button_press"] = current_time

    def s13_action(state, start_time, current_time):
      button_interval = 2
      if not "last_button_press" in state.data:
        state.data["last_button_press"] = start_time
      interval_since_last_press = (current_time - state.data["last_button_press"]).total_seconds()

      if interval_since_last_press > button_interval:
        self.client.press_X()
        state.data["last_button_press"] = current_time

    def s13_transition(state):
      return self.locations.menu_selection_arrow_location != None

    def s14_action(state, start_time, current_time):
      button_interval = 1
      if not "last_button_press" in state.data:
        state.data["last_button_press"] = start_time
      interval_since_last_press = (current_time - state.data["last_button_press"]).total_seconds()

      if not self.locations.menu_selection_arrow_location:
        return

      if interval_since_last_press > button_interval:
        target_y = 257
        target_x = 522
        min_box, max_box = self.locations.menu_selection_arrow_location
        if target_y > min_box[1] and target_y < max_box[1] and target_x > min_box[0] and target_x < max_box[0]:
          self.client.press_A()
        elif target_y < min_box[1]:
          self.client.press_Up()
        elif target_y > max_box[1]:
          self.client.press_Down()
        elif target_x < min_box[0]:
          self.client.press_Left()
        elif target_x > max_box[0]:
          self.client.press_Right()
        state.data["last_button_press"] = current_time

    def s14_transition(state):
      return self.locations.r_to_boxes_location != None

    def s15_action(state, start_time, current_time):
      button_interval = 3
      if not "last_button_press" in state.data:
        state.data["last_button_press"] = start_time
      interval_since_last_press = (current_time - state.data["last_button_press"]).total_seconds()

      if not self.locations.dialog_next_location:
        return

      if interval_since_last_press > button_interval:
        self.client.press_R()
        state.data["last_button_press"] = current_time

    def s15_transition(state):
      return self.locations.box_arrow_location != None

    def s16_action(state, start_time, current_time):
      button_interval = 1
      if not "last_button_press" in state.data:
        state.data["last_button_press"] = start_time
      interval_since_last_press = (current_time - state.data["last_button_press"]).total_seconds()

      if not self.locations.box_arrow_location:
        return

      if interval_since_last_press > button_interval:
        target_y = 361
        target_x = 147
        min_box, max_box = self.locations.box_arrow_location
        if target_y > min_box[1] and target_y < max_box[1] and target_x > min_box[0] and target_x < max_box[0]:
          state.data["go_to_next_step"] = True
        elif target_y < min_box[1]:
          self.client.press_Up()
        elif target_y > max_box[1]:
          self.client.press_Down()
        elif target_x < min_box[0]:
          self.client.press_Left()
        elif target_x > max_box[0]:
          self.client.press_Right()
        state.data["last_button_press"] = current_time

    def s16_transition(state):
      if not "go_to_next_step" in state.data:
        return False
      return state.data["go_to_next_step"]
  
    def s17_action(state, start_time, current_time):
      wait_time = 3
      interval = (current_time - start_time).total_seconds()
      target_x = 1849
      target_y = 192

      if self.locations.shiny_marker_location:
        min_box, max_box = self.locations.shiny_marker_location
        if target_y > min_box[1] and target_y < max_box[1] and target_x > min_box[0] and target_x < max_box[0]:
          state.data["is_shiny"] = True
      if interval > wait_time:
        print("Capture Screen to Check afterwards if algorithm is working as expected")
        state.data["go_to_next_step"] = True

    def s17_end_transition(state):
      if not "go_to_next_step" in state.data:
        return False
      if not "is_shiny" in state.data:
        return False
      return state.data["go_to_next_step"] and state.data["is_shiny"]
    
    def s17_reset_transition(state):
      if not "go_to_next_step" in state.data:
        return False
      return state.data["go_to_next_step"]

    def sEnd_action(state, start_time, current_time):
      if not "captured" in state.data:
        self.client.capture()
        state.data["captured"] = True
    
    def s18_action(state, start_time, current_time):
      button_interval = 2
      if not "last_button_press" in state.data:
        state.data["last_button_press"] = start_time
      interval_since_last_press = (current_time - state.data["last_button_press"]).total_seconds()

      if interval_since_last_press > button_interval:
        self.client.press_home()
        state.data["last_button_press"] = current_time

    def s18_transition(state):
      return self.locations.change_user_hint_location != None

    def s19_action(state, start_time, current_time):
      button_interval = 2
      if not "last_button_press" in state.data:
        state.data["last_button_press"] = start_time
      interval_since_last_press = (current_time - state.data["last_button_press"]).total_seconds()

      if interval_since_last_press > button_interval:
        self.client.press_Y()
        state.data["last_button_press"] = current_time

    def s19_transition(state):
      return self.locations.close_app_hint_location != None

    s1 = State("Opening Game, First Talk")
    s2 = State("Talking To Scientist, First Decision")
    s3 = State("Talking To Scientist, Second Decision")
    s4 = State("Talking To Scientist, Third Decision")
    s5 = State("Talking To Scientist, Fourth Decision")
    s6 = State("Receiving Pokemon, First Dialog")
    s7 = State("Receiving Pokemon, Second Dialog")
    s8 = State("Receiving Pokemon, Third Dialog")
    s9 = State("Receiving Pokemon, Fourth Dialog")
    s10 = State("Receiving Pokemon, Fifth Dialog")
    s11 = State("Receiving Pokemon, Sixth Dialog") # inverted
    s12 = State("Receiving Pokemon, Seventh Dialog") # inverted
    s13 = State("Open Menu")
    s14 = State("Open Pokemon")
    s15 = State("Open Boxes")
    s16 = State("Find Pokemon")
    s17 = State("Check Shinyness")
    sEnd = State("Is Shiny, Stop")
    s18 = State("Isn't Shiny, Reset")
    s19 = State("Change User")

    s1.set_action(s1_action)
    s1.add_transition(s2, s1_transition)

    s2.set_action(s2_action)
    s2.add_transition(s3, s2_to_5_transition)

    s3.set_action(s3_action)
    s3.add_transition(s4, s2_to_5_transition)

    s4.set_action(s4_action)
    s4.add_transition(s5, s2_to_5_transition)

    s5.set_action(s5_action)
    s5.add_transition(s6, s2_to_5_transition)

    s6.set_action(s6_to_10_action)
    s6.add_transition(s7, s6_to_10_transition)

    s7.set_action(s6_to_10_action)
    s7.add_transition(s8, s6_to_10_transition)

    s8.set_action(s6_to_10_action)
    s8.add_transition(s9, s6_to_10_transition)

    s9.set_action(s6_to_10_action)
    s9.add_transition(s10, s6_to_10_transition)

    s10.set_action(s6_to_10_action)
    s10.add_transition(s11, s6_to_10_transition)

    s11.set_action(s11_action)
    s11.add_transition(s12, s11_12_transition)

    s12.set_action(s12_action)
    s12.add_transition(s13, s11_12_transition)

    s13.set_action(s13_action)
    s13.add_transition(s14, s13_transition)

    s14.set_action(s14_action)
    s14.add_transition(s15, s14_transition)

    s15.set_action(s15_action)
    s15.add_transition(s16, s15_transition)
    
    s16.set_action(s16_action)
    s16.add_transition(s17, s16_transition)

    s17.set_action(s17_action)
    s17.add_transition(sEnd, s17_end_transition)
    s17.add_transition(s18, s17_reset_transition)

    sEnd.set_action(sEnd_action)

    s18.set_action(s18_action)
    s18.add_transition(s19, s18_transition)

    s19.set_action(s19_action)
    s19.add_transition(s1, s19_transition)

    return StateMachine(s1)
