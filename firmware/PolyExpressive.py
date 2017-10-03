#
# send MIDI to UART
from microWebSrv import MicroWebSrv
import gc
gc.collect()

from machine import UART
from machine import Timer
import I2CTouch
import ujson as json
import utime
### web stuff


uart = UART(1, 31250, tx=4)                         # init with given baudrate
uart.init(31250, bits=8, parity=None, stop=1) # init with given parameters
# pull these to global panel file so they can be shared
panel_x = 469 # factors 1, 7, 67
panel_y = 294 # factors 2, 3, 7, 7
grid_x = 33.5 # 14
grid_y = 42 # 7
num_x = int(panel_x/grid_x)

# action_list = []
current_action = None
end_action = None
clock_playing = False
clock_start = 0

# Used for debouncing
minimum_tap_interval = 60 * 1000 * 1000 * 1 / 300 # 300 is MAXIMUM_BPM;
maximum_tap_interval = 60 * 1000 * 1000 * 1 / 10 # 10 is minimum BPM
first_tap_time = 0
last_tap_time = 0
num_taps = 0

def calculate_interval_us(bpm):
    return 60 * 1000 * 1000 * 1 / bpm / 24;

clock_interval_us = calculate_interval_us(100) # 100 BPM 

action_list = []
with open('action_list.json', 'r') as f:
    action_list = json.load(f)

toggle_states = {}

MIDI_COMMANDS = {
        "clock": 0xF8,
        "start": 0xFA,
        "continue":0xFB,
        "stop": 0xFC
        }

def send_midi_message(command, data1, data2=0):
    uart.write(bytes((command, data1, data2)))

def send_clock_message(command):
    uart.write(bytes((command,)))

def transform_to_range(x, x1, x2):
    return ((x-x1) / (x2-x1)) * 127

def point_to_action(x, y, z):
    # search action list
    for a_id, action in enumerate(action_list):
        if (x >= action['x1'] and x < action['x2'] ) and (y >= action['y1'] and y < action['y2']):
            return (a_id, action)
    else:
        return (-1, False) # no actions defined for this region / error

# update firmware
#
# update action list / mat
def update_mat(new_action_list):
    # parse json file as the action list and mat def
    global action_list
    action_list = new_action_list
    toggle_states = {}
    with open('action_list.json', 'w') as f:
        f.write(json.dumps(action_list))

def lerp(start, end, t):
    return start+(end- start)*t

def evaluate_curve(curve, v):
    near = -1
    for i, p in enumerate(curve):
        if p[0] > v:
            near = i
            break
    if near < 0:
        # v larger than any x in curve, so set to end of curve
        return int(curve[-1][1])
    #curve[near-1], curve[near], v
    t = (v-curve[near-1][0]) / (curve[near][0] - curve[near-1][0])
    return int(lerp(curve[near-1][1], curve[near][1], t))

def map_and_send_midi(action, param):
    # evalate curve
    mapped_param = evaluate_curve(action['c'], param)
    # send MIDI with param
    send_midi_message(action["b1"], action["b2"], mapped_param)
    print("sending midi", action["b1"], action["b2"], mapped_param)

def update_bpm(bpm):
    global clock_interval_us
    clock_interval_us = calculate_interval_us(bpm)

def tap_tempo():
    MINIMUM_TAPS = 3
    EXIT_MARGIN = 150
    global first_tap_time
    global last_tap_time
    global num_taps
    # print("tapped for tempo")

    now = utime.ticks_us()
    if (now - last_tap_time < minimum_tap_interval):
        return # Debounce

    if (num_taps == 0):
        first_tap_time = now

    num_taps+=1
    last_tap_time = now

    if (num_taps > 0 and num_taps < MINIMUM_TAPS and (now - last_tap_time) > maximum_tap_interval):
        # Single taps, not enough to calculate a BPM -> ignore!
        num_taps = 0
    elif (num_taps >= MINIMUM_TAPS):
        avg_tap_interval = (last_tap_time - first_tap_time) / (num_taps - 1)
        # if ((now - last_tap_time) > (avg_tap_interval * EXIT_MARGIN / 100)):
        bpm = 60 * 1000 * 1000 * 1 / avg_tap_interval
        update_bpm(bpm)
        print("bpm is", bpm)
        num_taps = 0

def inner_execute_action(ap, z):
    global clock_playing
    global clock_start
    if ap["t"] == "start":
        send_clock_message(MIDI_COMMANDS["start"])
        clock_start = time.ticks_us()
        clock_playing = True
    if ap["t"] == "continue":
        send_clock_message(MIDI_COMMANDS["continue"])
        clock_start = time.ticks_us()
        clock_playing = True
    elif ap["t"] == "stop":
        send_clock_message(MIDI_COMMANDS["stop"])
        clock_start = 0
        clock_playing = False
    elif ap["t"] == "tap":
        tap_tempo()
    elif ap["t"] == "m":
        if "c" in ap:
            map_and_send_midi(ap, z)
        else:
            # send MIDI no parameters
            send_midi_message(ap["b1"], ap["b2"], ap["b3"])

def execute_continous_action(actions, x1, y1, x2, y2, x, y, z):
    if 'x' in actions:
        m_x = transform_to_range(x, x1, x2)
        for action in actions['x']:
            map_and_send_midi(action, m_x)
    elif 'y' in actions:
        m_y = transform_to_range(y, y1, y2)
        for action in actions['y']:
            map_and_send_midi(action, m_y)
    elif 'z' in actions:
        # z is already transformed to the currect range
        for action in actions['z']:
            map_and_send_midi(action, z)

def execute_action(actions, action_id, z):
    for ap in actions:
        if ap["t"] == 't': #toggle
            if action_id not in toggle_states: # this is initial, so invert initial state
                # invert it TODO allow different initial state than off
                toggle_states[action_id] = True
            else:
                toggle_states[action_id] = not toggle_states[action_id]
            if toggle_states[action_id]:
                inner_execute_action(ap["on"], z)
            else:
                inner_execute_action(ap["off"], z)
        else:
            inner_execute_action(ap, z)


def tick_midi_clock():
    global clock_start
    if clock_playing == True:
        delta = time.ticks_diff(time.ticks_us(), clock_start) # compute time difference
        if delta > clock_interval_us:
            clock_start = time.ticks_us()
            send_clock_message(MIDI_COMMANDS["clock"])
# main loop
def core_loop():
    # send clock first, if we're sending clock
    global end_action
    global current_action
    tick_midi_clock()

    point_available, x,y,m_z = I2CTouch.get_point()
    if point_available:
        z = transform_to_range(m_z, 0, 256)
        if z < 1.8: # invalid point
            # if there is end touch queued
            if end_action is not None:
                # run them
                execute_action(end_action, current_action['id'], 0)
                # print("executing end action, invalid point", current_action['id'])
                end_action = None
            current_action = None
        else:
            action_id, action = point_to_action(x, y, z)
            if action != False:
                if current_action is None or current_action['id'] != action_id: # compare id's
                    print("action occured", action_id)
                    # the new action isn't the same as the previous current action so execute any end_action
                    if end_action is not None:
                        # run them
                        # print("executing end action, got new action", current_action['id'])
                        execute_action(end_action, current_action['id'], z)
                        end_action = None
                    # got a valid point, if it's not executing at the moment then it's a start 
                    current_action = action
                    current_action['id'] = action_id
                    if "e" in action:
                        end_action = action["e"]
                    if "s" in action:
                        execute_action(action["s"], current_action['id'], z)
                else:
                    # otherwise it's an on change
                    if "c" in action:
                        execute_continous_action(action["c"], action['x1'], action['y1'], action['x2'], action['y2'], x, y, z)
                    # print("finger down pressure is", z)
            else:
                # end action
                if end_action is not None:
                    # run them
                    execute_action(end_action, current_action['id'], 0)
                    # print("executing end action, new action is false", current_action['id'])
                    end_action = None
                current_action = None


def run():
    while True:
        core_loop()
        utime.sleep_us(100)

    # Serve web pages / config update
    # anything else in the core loop?

#
# bluetooth / wifi chaining
# send MIDI to bluetooth BLE

def http_get_action_list(httpClient, httpResponse) :
    httpResponse.WriteResponseOk(None, "application/json", "UTF-8", json.dumps(action_list))

def http_update_action_list(httpClient, httpResponse) :
    # print("update action list")
    jdata  = httpClient.ReadRequestContent()
    content = False
    try:
        t_action_list = json.loads(jdata)
        # if it loads and has an action in it, it's valid
        t_action_list[0]['x1']
        update_mat(t_action_list)
        content = True
    except:
        content = False
    httpResponse.WriteResponseOk(None, "application/json", "UTF-8", json.dumps(content))


route_handlers = [
        ( "/get_action_list",      "GET",  http_get_action_list ),
        ( "/update_action_list",      "POST", http_update_action_list )
]

srv = MicroWebSrv(routeHandlers=route_handlers)
srv.Start(threaded=True)

# ----------------------------------------------------------------------------
