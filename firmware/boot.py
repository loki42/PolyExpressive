# boot.py -- run on boot-up
import network
import binascii
ap = network.WLAN(network.AP_IF) # create access-point interface
ap.active(True)

ap.config(essid="Poly-"+binascii.hexlify(ap.config("mac")).decode("ascii"), password="expressive", authmode=3)
