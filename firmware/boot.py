# boot.py -- run on boot-up
import network
ap = network.WLAN(network.AP_IF) # create access-point interface
ap.active(True)
ap.config(essid="Poly-"+str(ap.config("mac")[-1]), password="expressive", authmode=3)
