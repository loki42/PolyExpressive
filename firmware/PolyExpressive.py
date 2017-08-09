#
# send MIDI to UART
from machine import UART, Pin
import machine
from machine import Timer
uart = UART(1, 31250)                         # init with given baudrate
uart.init(31250, bits=8, parity=None, stop=1) # init with given parameters

# Define which pins are connected to what
# for resistive touch
YP = 'P20'  # must be an analog pin, ADC blue to red
XM = 'P19'  # must be an analog pin, ADC Green to black
YM = 'P22'   # can be a digital pin DAC Green to yellow
XP = 'P21' # can be a digital pin DAC white to orange
ATTN_11DB = 3


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
# For the one we're using, its TODO ohms across the X plate

# location to action

# continuous 



#XXX
def get_point():
    samples = [0, 0]
    valid = True
    default_high = 0.5
    NUM_SAMPLES = 2
    _rxplate = 0

    y_p = Pin(YP, mode=Pin.OUT)
    y_m = Pin(YM, mode=Pin.OUT)
    y_p.value(0)
    y_m.value(0)

    adc1 = machine.ADC()
    y_p = adc1.channel(pin=YP, attn=ATTN_11DB)

    x_p = Pin(XP, mode=Pin.OUT)
    x_m = Pin(XM, mode=Pin.OUT)

    x_p.value(1)
    x_m.value(0)

    # Fast ARM chips need to allow voltages to settle
    Timer.sleep_us(20)

    for i in range(NUM_SAMPLES):
        samples[i] = y_p()

    # Allow small amount of measurement noise, because capacitive
    # coupling to a TFT display's signals can induce some noise.
    if ((samples[0] - samples[1] < -4) or (samples[0] - samples[1] > 4)):
        valid = False
    else:
        samples[1] = (samples[0] + samples[1]) / 2 # average 2 samples
    print("x is", samples[1])
    x = (1023-samples[1])

    # same thing but for y

    adc1 = machine.ADC()
    x_m = adc1.channel(pin=XM, attn=ATTN_11DB)

    y_m = Pin(YM, mode=Pin.OUT)
    y_p = Pin(YP, mode=Pin.OUT)

    y_m.value(0)
    y_p.value(1)

    # Fast ARM chips need to allow voltages to settle
    Timer.sleep_us(20)

    for i in range(NUM_SAMPLES):
        samples[i] = x_m()

    # Allow small amount of measurement noise, because capacitive
    # coupling to a TFT display's signals can induce some noise.
    if ((samples[0] - samples[1] < -4) or (samples[0] - samples[1] > 4)):
        valid = False
    else:
        samples[1] = (samples[0] + samples[1]) / 2 # average 2 samples
    print("y is", samples[1])
    y = (1023-samples[1])

    # Set X+ to ground
    # Set Y- to VCC
    # Hi-Z X- and Y+
    x_p = Pin(XP, mode=Pin.OUT)
    y_m = Pin(YM, mode=Pin.OUT)
    adc1 = machine.ADC()
    y_p = adc1.channel(pin=YP, attn=ATTN_11DB)
    adc2 = machine.ADC()
    x_m = adc2.channel(pin=XM, attn=ATTN_11DB)

    x_p.value(0)
    y_m.value(1)

    z1 = x_m()
    z2 = y_p()

    z = 0
    if (_rxplate != 0):
        rtouch = z2
        rtouch /= z1
        rtouch -= 1
        rtouch *= x
        rtouch *= _rxplate
        rtouch /= 1024
        z = rtouch
    else:
        z = (1023-(z2-z1))
    if not valid:
        z = 0

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
