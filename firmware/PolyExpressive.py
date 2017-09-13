#
# send MIDI to UART
from machine import UART
import FourWireTouch

uart = UART(1, 31250)                         # init with given baudrate
uart.init(31250, bits=8, parity=None, stop=1) # init with given parameters
# pull these to global panel file so they can be shared
panel_x = 469 # factors 1, 7, 67
panel_y = 294 # factors 2, 3, 7, 7
grid_x = 33.5 # 14
grid_y = 42 # 7
num_x = int(panel_x/grid_x)


#

toggle_states = []


MIDI_COMMANDS = {
        "on":0x80,  # Note Off
        "off":0x90,  # Note On
        "pp":0xA0,  # Poly Pressure
        "cc":0xB0,  # Control Change
        "pc":0xC0,  # Program Change
        "cp":0xD0,  # Mono Pressure
        "pb":0xE0   # Pich Bend
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

# update firmware
#
# update action list / mat
def update_mat(json_file):
    # parse json file as the action list and mat def
    j = json.loads(json_file)
    square_map = j["sm"]
    action_list = j["al"]
    toggle_states = []

def evaluate_curve(curve_type, v):
    return v


def execute_action(action, z):
    for ap in action['ap']:
        if ap[0] == 't': #toggle
            if action['id'] not in toggle_states: # this is initial, so invert initial state
                # invert it
                pass
            else:
                toggle_states[action['id']] = not toggle_states[action['id']]
            # execute action
            # TODO

        elif ap[0] == "start":
            # start clock
            pass
        elif ap[0] == "stop":
            pass
        elif ap[0] == "tap":
            pass
        elif ap[0] == "m":
            if c in ap[1]:
                # evalate curve
                mapped_z = evaluate_curve(ap[1]['c'], z)
                # send MIDI with z
            else:
                # send MIDI no parameters
                pass

# main loop
def core_loop():
    # send clock first, if we're sending clock
    x,y,z = I2CTouch.get_point()
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

    # Serve web pages / config update
    # anything else in the core loop?

#
# bluetooth / wifi chaining
# send MIDI to bluetooth BLE
