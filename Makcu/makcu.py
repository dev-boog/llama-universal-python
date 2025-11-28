import time
import serial
import serial.tools.list_ports

import threading

class Makcu:
    baud_change_command = bytearray([0xDE, 0xAD, 0x05, 0x00, 0xA5, 0x00, 0x09, 0x3D, 0x00])
    ser = None
    button_states = {"LMB": False, "RMB": False}
    is_connected = False
    _listener_thread = None

    @staticmethod
    def MoveMouse(x, y):
        cmd = f"km.move({x},{y})\r".encode() 
        try:
            if Makcu.ser:
                Makcu.ser.write(cmd)
                Makcu.ser.flush()
        except Exception as e:
            print(e)

    @staticmethod   
    def FindCOMPort():
        for port in serial.tools.list_ports.comports():
            if "1A86" in port.hwid and "55D3" in port.hwid:
                return port.device
        return None

    @staticmethod
    def Connect():
        com_port = Makcu.FindCOMPort()
        if not com_port:
            print("Makcu not found") 
            return False
        
        try:
            Makcu.ser = serial.Serial(com_port, 115200, timeout=1)
            time.sleep(0.1)
            Makcu.ser.write(Makcu.baud_change_command)
            Makcu.ser.close()
            
            Makcu.ser = serial.Serial(com_port, 4000000, timeout=1)
            time.sleep(0.1)
            Makcu.ser.write(b"km.buttons(1)\r")
            Makcu.ser.write(b"km.echo(0)\r")
            Makcu.ser.reset_input_buffer()

            Makcu.is_connected = True
            return True
        except Exception as e:
            print(f"Makcu connection error: {str(e)}")
            Makcu.is_connected = False
            return False

    @staticmethod
    def _button_listener():
        valid_bytes = {0x00, 0x01, 0x02, 0x03}
        prev_lmb = prev_rmb = None
        
        while True:
            if not Makcu.is_connected:
                time.sleep(1)
                continue
            
            try:
                if Makcu.ser and Makcu.ser.in_waiting > 0:
                    raw = Makcu.ser.read(1)
                    byte = ord(raw)
                    
                    if byte not in valid_bytes:
                        continue
                    
                    Makcu.button_states["LMB"] = bool(byte & 0b00000001)
                    Makcu.button_states["RMB"] = bool(byte & 0b00000010)
                    
                    # if Makcu.button_states["LMB"] != prev_lmb:
                        # print(f"[Makcu] LMB: {'pressed' if Makcu.button_states['LMB'] else 'released'}")
                    # if Makcu.button_states["RMB"] != prev_rmb:
                        # print(f"[Makcu] RMB: {'pressed' if Makcu.button_states['RMB'] else 'released'}")
                    
                    prev_lmb = Makcu.button_states["LMB"]
                    prev_rmb = Makcu.button_states["RMB"]
                    
                    Makcu.ser.reset_input_buffer()
                    
            except Exception as e:
                print(f"Makcu button listener error: {str(e)}")
                Makcu.is_connected = False

    @staticmethod
    def StartButtonListener():
        if Makcu._listener_thread is None or not Makcu._listener_thread.is_alive():
            Makcu._listener_thread = threading.Thread(target=Makcu._button_listener, daemon=True)
            Makcu._listener_thread.start()

    @staticmethod
    def GetButtonState(button):
        return Makcu.button_states.get(button, False)

    @staticmethod
    def Disconnect():
        Makcu.is_connected = False
        if Makcu.ser:
            try:
                Makcu.ser.close()
            except:
                pass