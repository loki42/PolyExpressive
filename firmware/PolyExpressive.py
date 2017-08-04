#
# send MIDI to UART
from machine import UART
uart = UART(1, 31250)                         # init with given baudrate
uart.init(31250, bits=8, parity=None, stop=1) # init with given parameters

# Define which pins are connected to what
# for resistive touch
YP = 2  # must be an analog pin, use "An" notation!
XM = 3  # must be an analog pin, use "An" notation!
YM = 8   # can be a digital pin
XP = 9 # can be a digital pin


MIDI_COMMANDS = {
        "note_on":0x80,  # Note Off
        "note_off":0x90,  # Note On
        "poly_pressure":0xA0,  # Poly Pressure
        "cc":0xB0,  # Control Change
        "pc":0xC0,  # Program Change
        "channel_pressure":0xD0,  # Mono Pressure
        "pitch_bend":0xE0   # Pich Bend
)

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
    samples = []
    valid = 1
"""
TSPoint TouchScreen::getPoint(void) {
  int x, y, z;
  int samples[NUMSAMPLES];
  uint8_t i, valid;

  valid = 1;

  pinMode(_yp, INPUT);
  pinMode(_ym, INPUT);
  pinMode(_xp, OUTPUT);
  pinMode(_xm, OUTPUT);

#if defined (USE_FAST_PINIO)
  *xp_port |= xp_pin;
  *xm_port &= ~xm_pin;
#else
  digitalWrite(_xp, HIGH);
  digitalWrite(_xm, LOW);
#endif

#ifdef __arm__
  delayMicroseconds(20); // Fast ARM chips need to allow voltages to settle
#endif

   for (i=0; i<NUMSAMPLES; i++) {
     samples[i] = analogRead(_yp);
   }

#if NUMSAMPLES > 2
   insert_sort(samples, NUMSAMPLES);
#endif
#if NUMSAMPLES == 2
   // Allow small amount of measurement noise, because capacitive
   // coupling to a TFT display's signals can induce some noise.
   if (samples[0] - samples[1] < -4 || samples[0] - samples[1] > 4) {
     valid = 0;
   } else {
     samples[1] = (samples[0] + samples[1]) >> 1; // average 2 samples
   }
#endif

   x = (1023-samples[NUMSAMPLES/2]);

   pinMode(_xp, INPUT);
   pinMode(_xm, INPUT);
   pinMode(_yp, OUTPUT);
   pinMode(_ym, OUTPUT);

#if defined (USE_FAST_PINIO)
   *ym_port &= ~ym_pin;
   *yp_port |= yp_pin;
#else
   digitalWrite(_ym, LOW);
   digitalWrite(_yp, HIGH);
#endif

  
#ifdef __arm__
   delayMicroseconds(20); // Fast ARM chips need to allow voltages to settle
#endif

   for (i=0; i<NUMSAMPLES; i++) {
     samples[i] = analogRead(_xm);
   }

#if NUMSAMPLES > 2
   insert_sort(samples, NUMSAMPLES);
#endif
#if NUMSAMPLES == 2
   // Allow small amount of measurement noise, because capacitive
   // coupling to a TFT display's signals can induce some noise.
   if (samples[0] - samples[1] < -4 || samples[0] - samples[1] > 4) {
     valid = 0;
   } else {
     samples[1] = (samples[0] + samples[1]) >> 1; // average 2 samples
   }
#endif

   y = (1023-samples[NUMSAMPLES/2]);

   // Set X+ to ground
   // Set Y- to VCC
   // Hi-Z X- and Y+
   pinMode(_xp, OUTPUT);
   pinMode(_yp, INPUT);

#if defined (USE_FAST_PINIO)
   *xp_port &= ~xp_pin;
   *ym_port |= ym_pin;
#else
   digitalWrite(_xp, LOW);
   digitalWrite(_ym, HIGH); 
#endif
  
   int z1 = analogRead(_xm); 
   int z2 = analogRead(_yp);

   if (_rxplate != 0) {
     // now read the x 
     float rtouch;
     rtouch = z2;
     rtouch /= z1;
     rtouch -= 1;
     rtouch *= x;
     rtouch *= _rxplate;
     rtouch /= 1024;
     
     z = rtouch;
   } else {
     z = (1023-(z2-z1));
   }

   if (! valid) {
     z = 0;
   }

   return TSPoint(x, y, z);
}

TouchScreen::TouchScreen(uint8_t xp, uint8_t yp, uint8_t xm, uint8_t ym,
			 uint16_t rxplate=0) {
  _yp = yp;
  _xm = xm;
  _ym = ym;
  _xp = xp;
  _rxplate = rxplate;

#if defined (USE_FAST_PINIO)
  xp_port =  portOutputRegister(digitalPinToPort(_xp));
  yp_port =  portOutputRegister(digitalPinToPort(_yp));
  xm_port =  portOutputRegister(digitalPinToPort(_xm));
  ym_port =  portOutputRegister(digitalPinToPort(_ym));
  
  xp_pin = digitalPinToBitMask(_xp);
  yp_pin = digitalPinToBitMask(_yp);
  xm_pin = digitalPinToBitMask(_xm);
  ym_pin = digitalPinToBitMask(_ym);
#endif

  pressureThreshhold = 10;
}

int TouchScreen::readTouchX(void) {
   pinMode(_yp, INPUT);
   pinMode(_ym, INPUT);
   digitalWrite(_yp, LOW);
   digitalWrite(_ym, LOW);
   
   pinMode(_xp, OUTPUT);
   digitalWrite(_xp, HIGH);
   pinMode(_xm, OUTPUT);
   digitalWrite(_xm, LOW);
   
   return (1023-analogRead(_yp));
}


int TouchScreen::readTouchY(void) {
   pinMode(_xp, INPUT);
   pinMode(_xm, INPUT);
   digitalWrite(_xp, LOW);
   digitalWrite(_xm, LOW);
   
   pinMode(_yp, OUTPUT);
   digitalWrite(_yp, HIGH);
   pinMode(_ym, OUTPUT);
   digitalWrite(_ym, LOW);
   
   return (1023-analogRead(_xm));
}


uint16_t TouchScreen::pressure(void) {
  // Set X+ to ground
  pinMode(_xp, OUTPUT);
  digitalWrite(_xp, LOW);
  
  // Set Y- to VCC
  pinMode(_ym, OUTPUT);
  digitalWrite(_ym, HIGH); 
  
  // Hi-Z X- and Y+
  digitalWrite(_xm, LOW);
  pinMode(_xm, INPUT);
  digitalWrite(_yp, LOW);
  pinMode(_yp, INPUT);
  
  int z1 = analogRead(_xm); 
  int z2 = analogRead(_yp);

  if (_rxplate != 0) {
    // now read the x 
    float rtouch;
    rtouch = z2;
    rtouch /= z1;
    rtouch -= 1;
    rtouch *= readTouchX();
    rtouch *= _rxplate;
    rtouch /= 1024;
    
    return rtouch;
  } else {
    return (1023-(z2-z1));
  }

}
"""
#XXX

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
