from state_machine import State, StateMachine 

s1 = State("state1")
s2 = State("state2")

def action1(state, start_time, cur_time):
  print(state == s1)
  print(start_time)
  print(cur_time)
  print("action1")


def condition1(a):
  print(a)
  return True

s1.set_action(action1)
s1.add_transition(s2, condition1)

s2.set_action(action1)

sm = StateMachine(s1)

sm.step()
sm.step()