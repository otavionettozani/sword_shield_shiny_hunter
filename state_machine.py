from datetime import datetime

class State:
  def __init__(self, name):
    self.name = name
    self.next_states = []
    self.next_states_conditions = []
    self.action = None
    self.on_enter = None
    self.on_exit = None
    self.start_time = None
    self.data = None

  def add_transition(self, next_state, condition):
    self.next_states.append(next_state)
    self.next_states_conditions.append(condition)
  
  def set_action(self, action):
    self.action = action

  def set_on_enter(self, action):
    self.on_enter = action

  def set_on_exit(self, action):
    self.on_exit = action

  def _action(self):
    if self.action != None:
      self.action(self, self.start_time, datetime.now())

  def _on_enter(self):
    print(f"Entering {self.name}")
    self.start_time = datetime.now()
    self.data = {}
    if self.on_enter != None:
      self.on_enter(self, self.start_time)

  def _on_exit(self):
    if self.on_exit != None:
      self.on_exit(self, self.start_time, datetime.now())
    self.start_time = None
    self.data = None
    print(f"Exiting {self.name}")



class StateMachine:
  def __init__(self, initial_state):
    self.initial_state = initial_state
    self.current_state = initial_state
    self.started = False

  def step(self):
    if not self.started:
      self.started = True
      self.initial_state._on_enter()

    self.current_state._action()

    i = 0
    for condition in self.current_state.next_states_conditions:
      if condition(self.current_state):
        last_state = self.current_state
        self.current_state = self.current_state.next_states[i]
        last_state._on_exit()
        self.current_state._on_enter()
        break
      else:
        i += 1