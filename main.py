import os
import sys
import subprocess
import logging

def install_requirements():
    """Auto-install missing packages from requirements.txt"""
    requirements_file = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(requirements_file):
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', requirements_file])
        except subprocess.CalledProcessError:
            print("Failed to install requirements")
            sys.exit(1)

install_requirements()

logging.getLogger("werkzeug").handlers.clear()
logging.getLogger("werkzeug").addHandler(logging.NullHandler())
logging.getLogger("werkzeug").setLevel(logging.CRITICAL + 1)
logging.getLogger("werkzeug").propagate = False

from flask import Flask, render_template
from routes.control import control_bp
from routes.custom_patterns import patterns_bp

from colorama import init, Fore, Style
init(autoreset=True) 

from Makcu.makcu import Makcu
from Recoil.recoil import Recoil
import threading
import time
import socket

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def create_app():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"""{Fore.CYAN}
            ____                         __  __      _                            __
           / / /___ _____ ___  ____ _   / / / /___  (_)   _____  ______________ _/ /
          / / / __ `/ __ `__ \/ __ `/  / / / / __ \/ / | / / _ \/ ___/ ___/ __ `/ / 
         / / / /_/ / / / / / / /_/ /  / /_/ / / / / /| |/ /  __/ /  (__  ) /_/ / /  
        /_/_/\__,_/_/ /_/ /_/\__,_/   \____/_/ /_/_/ |___/\___/_/  /____/\__,_/_/   
    {Style.RESET_ALL}""")
    print(f"\n[{Fore.CYAN}+{Style.RESET_ALL}] {Fore.CYAN}Status: {Style.RESET_ALL}Connected")
    print(f"[{Fore.CYAN}+{Style.RESET_ALL}] {Fore.CYAN}Web GUI: {Style.RESET_ALL}http://{get_local_ip()}:5000")

    app = Flask(__name__)
    app.register_blueprint(control_bp)
    app.register_blueprint(patterns_bp)

    @app.route('/')
    def index():
        return render_template('index.html',
            mode=Recoil.mode,
            enabled=Recoil.enabled,
            x=Recoil.x,
            y=Recoil.y,
            delay=Recoil.delay,
            pattern_enabled=Recoil.pattern_enabled,
            pattern=[{"x": x, "y": y} for x, y in Recoil.pattern]
        )
    return app

def makcu_loop():
    connected = Makcu.Connect()
    if connected:
        Makcu.StartButtonListener()
        try:
            while True:
                Recoil.RecoilLoop()
                time.sleep(0.001)
        except KeyboardInterrupt:
            Makcu.Disconnect()

if __name__ == "__main__":
    import sys
    from io import StringIO

    threading.Thread(target=makcu_loop, daemon=True).start()
    app = create_app()

    old_stdout = sys.stdout
    sys.stdout = StringIO()

    try:
        app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False, threaded=True)
    finally:
        sys.stdout = old_stdout
