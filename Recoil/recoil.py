from Makcu.makcu import Makcu
import time
import math
import random
from perlin_noise import PerlinNoise

class Recoil:
    mode = "Simple" 

    enabled = True
    x = 0
    y = 0
    delay = 0.01
    ShotCount = 0
    
    pattern_enabled = False
    pattern = []  
    
    @staticmethod
    def ease_out_quad(t):
        return t * (2 - t)

    @staticmethod
    def move_mouse_smoothly(dx, dy, duration=0.133, steps=20):
        if dx == 0 and dy == 0:
            return

        current_x, current_y = 0, 0
        noise_x = PerlinNoise(octaves=2, seed=random.randint(1, 10000))
        noise_y = PerlinNoise(octaves=2, seed=random.randint(1, 10000))

        for i in range(steps):
            t = (i + 1) / steps
            eased_t = Recoil.ease_out_quad(t)

            target_step_x = dx * eased_t
            target_step_y = dy * eased_t

            move_this_step_x = target_step_x - current_x
            move_this_step_y = target_step_y - current_y

            jitter_x = noise_x(i * 0.5) * random.uniform(0.1, 0.5)
            jitter_y = noise_y(i * 0.5) * random.uniform(0.1, 0.5)

            final_x = int(move_this_step_x + jitter_x)
            final_y = int(move_this_step_y + jitter_y)

            Makcu.MoveMouse(final_x, final_y)

            current_x += final_x
            current_y += final_y

            time.sleep(duration / steps)

    @staticmethod
    def RecoilLoop():
        if Makcu.GetButtonState("RMB") and Makcu.GetButtonState("LMB") and Recoil.enabled:
            if Recoil.mode == "Advanced" and Recoil.pattern_enabled and Recoil.pattern:
                if Recoil.ShotCount < len(Recoil.pattern):
                    x_val, y_val = Recoil.pattern[Recoil.ShotCount]
                    x_val *= 1.2
                    y_val *= 1.2 
                    Recoil.move_mouse_smoothly(x_val, y_val, duration=Recoil.delay)
                    Recoil.ShotCount += 1       
            elif Recoil.mode == "Simple":
                Recoil.move_mouse_smoothly(Recoil.x, Recoil.y, duration=Recoil.delay)
                Recoil.ShotCount += 1
        else:
            Recoil.ShotCount = 0
