#!/usr/bin/python3
""" Test delete feature
"""
from models.engine.file_storage import FileStorage
from models.state import State

fs = FileStorage()

fs._FileStorage__objects = {}
fs.save()

# All States
all_states = fs.all()
print("All States: {}".format(len(all_states.keys())))

# Create a new State
new_state = State()
new_state.name = "California"
fs.new(new_state)
fs.save()  # Save the new state

# Print the new state
print("New State: {}".format(new_state))

# All States after adding new_state
all_states = fs.all()
print("All States: {}".format(len(all_states.keys())))
for state_key in all_states.keys():
    print(all_states[state_key])

# Create another State
another_state = State()
another_state.name = "Nevada"
fs.new(another_state)
fs.save()
print("Another State: {}".format(another_state))

# All States after adding another_state
all_states = fs.all()
print("All States: {}".format(len(all_states.keys())))
for state_key in all_states.keys():
    print(all_states[state_key])

# Delete the new State
fs.delete(new_state)
fs.save()

# All States after deleting new_state
all_states = fs.all()
print("All States: {}".format(len(all_states.keys())))
for state_key in all_states.keys():
    print(all_states[state_key])
