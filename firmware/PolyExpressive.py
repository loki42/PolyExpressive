#
# send MIDI to UART
from machine import UART
import FourWireTouch

uart = UART(1, 31250)                         # init with given baudrate
uart.init(31250, bits=8, parity=None, stop=1) # init with given parameters
grid_x = 70
grid_y = 99
width_x = 420
num_x = int(420/70)


MIDI_COMMANDS = {
        "note_on":0x80,  # Note Off
        "note_off":0x90,  # Note On
        "poly_pressure":0xA0,  # Poly Pressure
        "cc":0xB0,  # Control Change
        "pc":0xC0,  # Program Change
        "channel_pressure":0xD0,  # Mono Pressure
        "pitch_bend":0xE0   # Pich Bend
        }

on_bytes =  bytes((0x90, 0x3C, 0x7A))
off_bytes =  bytes((0x80, 0x3C, 0x7A))

# for i in range(20):
#     PolyExpressive.uart.write(on_bytes)
#     time.sleep(0.5)
#     PolyExpressive.uart.write(off_bytes)
#     time.sleep(0.5)

def send_midi_message(channel, command, data1, data2=0):
    command += self.channel - 1
    uart.write(bytes((command, data1, data2)))


def square_to_action(x, y, z):
    index = int(x/grid_x) + (int(y/grid_y) * num_x)

# toggle 
#
# update firmware
#
# update action list / mat
def update_mat(json_file):
    # parse json file as the action list and mat def
    # format is [{index:action}, {action_id:[list_of_action]}
    # action triggers are
    # on_start_touch shown as s
    # on_end_touch shown as e
    # on_change shown as c
    # actions are
    # send midi
    # send midi and toggle state [on_off, on_on, initial]
    # start sending clock
    # stop sending clock
    # tap temp clock
    # start and end can use pressure (x)
    # change can use x, y, z
    # curve options - if no curve then takes no params
    # cartmull rom / hermite
    # {"x":{'curve_type':'c', v:[[in, out], ]}, "y": etc}
    pass

def execute_action(action):
    pass


# main loop
def core_loop():
    # send clock first, if we're sending clock
    x,y,z = FourWireTouch.get_point()
    action = square_to_action(x, y, z)
    if z == 0: # invalid point
        # if there is end touch queued
        if end_action not None:
            end_action = None
            # run them
            execute_action(end_action)
    else:
        if current_action['id'] != action['id']: # compare id's
            # the new action isn't the same as the previous current action so execute any end_action
            if end_action not None:
                end_action = None
                # run them
                execute_action(end_action, z)
            # got a valid point, if it's not executing at the moment then it's a start 
            current_action = action
            if "e" in action:
                end_action = action["e"]
            if "s" in action:
                execute_action(action["s"], z)
        else:
            # otherwise it's an on change
            if "c" in action:
                execute_continous_action(action["c"], x, y, z)
# get_point()
# 

#
# bluetooth / wifi chaining
#
# Serve web pages / config update

# send MIDI to bluetooth BLE
