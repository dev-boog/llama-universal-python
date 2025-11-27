from Makcu.makcu import Makcu
import time

class Recoil:
    mode = "Simple" 

    enabled = True
    x = 0
    y = 0
    delay = 0.01
    ShotCount = 0
    
    pattern_enabled = False
    pattern = []  
    
    def RecoilLoop():
        if Makcu.GetButtonState("RMB") and Makcu.GetButtonState("LMB") and Recoil.enabled:
            if Recoil.mode == "Advanced" and Recoil.pattern_enabled and Recoil.pattern:
                if Recoil.ShotCount < len(Recoil.pattern):
                    x_val, y_val = Recoil.pattern[Recoil.ShotCount]
                    Makcu.MoveMouse(x_val, y_val)
                    Recoil.ShotCount += 1
                    time.sleep(Recoil.delay)       
            elif Recoil.mode == "Simple":
                Makcu.MoveMouse(Recoil.x, Recoil.y)
                Recoil.ShotCount += 1
                time.sleep(Recoil.delay)
        else:
            Recoil.ShotCount = 0


if __name__ == "__main__":
    def main():
        Makcu.Connect()
        while True:
            Recoil.RecoilLoop()
    main()