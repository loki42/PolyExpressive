from machine import Pin
import machine
from machine import Timer

ATTN_11DB = 3
# Define which pins are connected to what
# for resistive touch
# wipy
# YP = 'P20'  # must be an analog pin, ADC blue to red
# XM = 'P19'  # must be an analog pin, ADC Green to black
# YM = 'P22'   # can be a digital pin DAC Green to yellow
# XP = 'P21' # can be a digital pin DAC white to orange

# wroom
YP = 'P18'  # must be an analog pin, ADC blue to red
XM = 'P17'  # must be an analog pin, ADC Green to black
YM = 'P20'   # can be a digital pin DAC Green to yellow
XP = 'P19' # can be a digital pin DAC white to orange

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
    adc1 = machine.ADC()
    y_p = adc1.channel(pin=YP, attn=ATTN_11DB)
    y_m = Pin(YM, mode=Pin.IN)

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
    x = (4095-samples[1])

    # same thing but for y
    # Timer.sleep_us(20)

    x_p = Pin(XP, mode=Pin.IN)
    x_m = Pin(XM, mode=Pin.IN)
    adc2 = machine.ADC()
    x_m = adc2.channel(pin=XM, attn=ATTN_11DB)
    x_p = Pin(XP, mode=Pin.IN)


    y_m = Pin(YM, mode=Pin.OUT)
    y_p = Pin(YP, mode=Pin.OUT)

    y_p.value(1)
    y_m.value(0)

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
    y = (4095-samples[1])
    # return y

    # Set X+ to ground
    # Set Y- to VCC
    # Hi-Z X- and Y+
    x_m = Pin(XM, mode=Pin.IN)
    y_p = Pin(YP, mode=Pin.IN)

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

