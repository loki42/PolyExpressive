# check if update exists, if it does, check it it works, otherwise delete it and run previous
import uos
try:
    uos.stat("update_firmware.py")
    print("update file exists")
    try:
        import update_firmware
        update_firmware.run()
    except:
        uos.remove("update_firmware.py")
        print("removing update")
except OSError:
    pass

import PolyExpressive
PolyExpressive.run()

