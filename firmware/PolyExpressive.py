#
# send MIDI to UART
from microWebSrv import MicroWebSrv
import gc
gc.collect()

from machine import UART
from machine import Timer
import I2CTouch
import json
### web stuff


uart = UART(1, 31250)                         # init with given baudrate
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

action_list = [{"x1":0, "y1":0, "x2": 60, "y2": 60,
"s":[{"t":"m", "b1":144, "b2":60, "b3":113}], "e":[{"t":"m", "b1":144, "b2":60, "b3":0}]},
{"x1":60, "y1":0, "x2": 120, "y2": 60,
"c":{"x":[{"c":[[0,0], [127,127]], "b1":176, "b2":5}]}
},
{"x1":120, "y1":0, "x2": 180, "y2": 60,
"s":[{"t":"t", "on":{"t":"m", "b1":144, "b2":61, "b3":113}, "off":{"t":"m", "b1":144, "b2":61, "b3":0}}]
}
]
#

toggle_states = {}


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

def send_midi_message(command, data1, data2=0):
    uart.write(bytes((command, data1, data2)))

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
def update_mat(json_file):
    # parse json file as the action list and mat def
    j = json.loads(json_file)
    action_list = j["al"]
    toggle_states = {}

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

def inner_execute_action(ap, z):
    if ap["t"] == "start":
        # start clock
        pass
    elif ap["t"] == "stop":
        pass
    elif ap["t"] == "tap":
        pass
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


# main loop
def core_loop():
    # send clock first, if we're sending clock
    global end_action
    global current_action

    x,y,m_z = I2CTouch.get_point()
    z = transform_to_range(m_z, 0, 4095)
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
        Timer.sleep_us(100)

    # Serve web pages / config update
    # anything else in the core loop?

#
# bluetooth / wifi chaining
# send MIDI to bluetooth BLE


# ----------------------------------------------------------------------------

def _httpHandlerTestGet(httpClient, httpResponse) :
        content = """\
                True
        """
        httpResponse.WriteResponseOk( headers            = None,
                                                                  contentType    = "text/html",
                                                                  contentCharset = "UTF-8",
                                                                  content                = content )

def _httpHandlerTestPost(httpClient, httpResponse) :
        formData  = httpClient.ReadRequestPostedFormData()
        firstname = formData["firstname"]
        lastname  = formData["lastname"]
        content   = """\
        <!DOCTYPE html>
        <html lang=fr>
        <body>
            Firstname = %s<br />
            Lastname = %s<br />
        </body>
    </html>
        """ % ( firstname,
                    lastname )
        httpResponse.WriteResponseOk( headers            = None,
                                                                  contentType    = "text/html",
                                                                  contentCharset = "UTF-8",
                                                                  content                = content )


# ----------------------------------------------------------------------------

routeHandlers = [
        ( "/test",      "GET",  _httpHandlerTestGet ),
        ( "/test",      "POST", _httpHandlerTestPost )
]

srv = MicroWebSrv(routeHandlers=routeHandlers)
srv.Start(threaded=True)

# ----------------------------------------------------------------------------
