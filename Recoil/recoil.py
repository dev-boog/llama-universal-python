from Makcu.makcu import Makcu
import time

class Recoil:
    enabled = True
    x = 0
    y = 0
    delay = 0.01
    ShotCount = 0

    def RecoilLoop():
        if Makcu.GetButtonState("RMB") and Makcu.GetButtonState("LMB") and Recoil.enabled:               
            Makcu.MoveMouse(Recoil.x, Recoil.y)
            Recoil.ShotCount += 1
            time.sleep(Recoil.delay)
        else:
            Recoil.ShotCount = 0