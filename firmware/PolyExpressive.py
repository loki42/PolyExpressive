#
# send MIDI to UART
from machine import UART, Pin
import machine
import utime
uart = UART(1, 31250)                         # init with given baudrate
uart.init(31250, bits=8, parity=None, stop=1) # init with given parameters

# Define which pins are connected to what
# for resistive touch
# wipy
# YP = 'P20'  # must be an analog pin, ADC blue to red
# XM = 'P19'  # must be an analog pin, ADC Green to black
# YM = 'P22'   # can be a digital pin DAC Green to yellow
# XP = 'P21' # can be a digital pin DAC white to orange
ATTN_11DB = 3

# wroom
YP = 33  # must be an analog pin, ADC blue to red
XM = 32  # must be an analog pin, ADC Green to black
YM = 25   # can be a digital pin DAC Green to yellow
XP = 26 # can be a digital pin DAC white to orange

MIDI_COMMANDS = {
        "note_on":0x80,  # Note Off
        "note_off":0x90,  # Note On
        "poly_pressure":0xA0,  # Poly Pressure
        "cc":0xB0,  # Control Change
        "pc":0xC0,  # Program Change
        "channel_pressure":0xD0,  # Mono Pressure
        "pitch_bend":0xE0   # Pich Bend
        }

# on_bytes =  bytes((0x90, 0x3C, 0x7A))
# off_bytes =  bytes((0x80, 0x3C, 0x7A))

# for i in range(20):
#     uart.write(on_bytes)
#     time.sleep(0.5)
#     uart.write(off_bytes)
#     time.sleep(0.5)

def send_midi_message(channel, command, data1, data2=0):
    command += self.channel - 1
    uart.write(bytes((command, data1, data2)))


# TSPoint p = ts.getPoint();
#   // we have some minimum pressure we consider 'valid'
#   // pressure of 0 means no pressing!
# if (p.z > ts.pressureThreshhold) 

# Resistive Touch to coordinate / pressure
# use differentional config not single ended
# setting time
# 

# For better pressure precision, we need to know the resistance
# between X+ and X- Use any multimeter to read it
# For the one we're using, its 600 ohms across the X plate

# location to action

# continuous 



def get_point():
    samples = [0, 0]
    valid = True
    NUM_SAMPLES = 2
    _rxplate = 592
    x = 0

    y_m = Pin(YM, mode=Pin.IN)
    y_p = Pin(YP, mode=Pin.IN)
    y_p = machine.ADC(machine.Pin(YP), atten=machine.ADC.ATTN_11DB)
    y_m = Pin(YM, mode=Pin.IN)

    x_p = Pin(XP, mode=Pin.OUT)
    x_m = Pin(XM, mode=Pin.OUT)

    x_p.value(1)
    x_m.value(0)

    # Fast ARM chips need to allow voltages to settle
    utime.sleep_us(20)

    for i in range(NUM_SAMPLES):
        samples[i] = y_p.read()

    # Allow small amount of measurement noise, because capacitive
    # coupling to a TFT display's signals can induce some noise.
    if ((samples[0] - samples[1] < -4) or (samples[0] - samples[1] > 4)):
        valid = False
    else:
        samples[1] = (samples[0] + samples[1]) / 2 # average 2 samples
    print("x is", samples[1])
    x = (4095-samples[1])

    # same thing but for y
    # Timer.sleep_us(20)

    x_p = Pin(XP, mode=Pin.IN)
    x_m = Pin(XM, mode=Pin.IN)
    x_m = machine.ADC(machine.Pin(XM), atten=machine.ADC.ATTN_11DB)
    x_p = Pin(XP, mode=Pin.IN)


    y_m = Pin(YM, mode=Pin.OUT)
    y_p = Pin(YP, mode=Pin.OUT)

    y_p.value(1)
    y_m.value(0)

    # Fast ARM chips need to allow voltages to settle
    utime.sleep_us(20)

    for i in range(NUM_SAMPLES):
        samples[i] = x_m.read()

    # Allow small amount of measurement noise, because capacitive
    # coupling to a TFT display's signals can induce some noise.
    if ((samples[0] - samples[1] < -4) or (samples[0] - samples[1] > 4)):
        valid = False
    else:
        samples[1] = (samples[0] + samples[1]) / 2 # average 2 samples
    print("y is", samples[1])
    y = (4095-samples[1])
    # return y

    # Set X+ to ground
    # Set Y- to VCC
    # Hi-Z X- and Y+
    x_m = Pin(XM, mode=Pin.IN)
    y_p = Pin(YP, mode=Pin.IN)

    x_p = Pin(XP, mode=Pin.OUT)
    y_m = Pin(YM, mode=Pin.OUT)
    y_p = machine.ADC(machine.Pin(YP), atten=machine.ADC.ATTN_11DB)
    x_m = machine.ADC(machine.Pin(XM), atten=machine.ADC.ATTN_11DB)

    x_p.value(0)
    y_m.value(1)

    z1 = x_m.read()
    z2 = y_p.read()

    z = 0
    if (_rxplate != 0 and z1 != 0):
        rtouch = z2
        rtouch /= z1
        rtouch -= 1
        rtouch *= x
        rtouch *= _rxplate
        rtouch /= 4095
        z = rtouch
    else:
        z = (4095-(z2-z1))
    if not valid:
        print ("not valid")
        z = 0
    print("z is ", z)
    return (x, y, z)

# toggle 
#
# update firmware
#
# update action list?
#
# bluetooth / wifi chaining
#
# Serve web pages / config update

# send MIDI to bluetooth BLE
