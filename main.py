from Makcu.makcu import Makcu
from Recoil.recoil import Recoil

from flask import Flask, render_template, request, jsonify
import time
import threading

app = Flask(__name__)

@app.route('/update', methods=['POST'])
def update():
    data = request.get_json()

    Recoil.enabled = bool(data.get("enabled", Recoil.enabled))
    Recoil.x = float(data.get("x", Recoil.x))
    Recoil.y = float(data.get("y", Recoil.y))
    Recoil.delay = float(data.get("delay", Recoil.delay))

    return jsonify({
        "status": "success",
        "enabled": Recoil.enabled,
        "x": Recoil.x,
        "y": Recoil.y,
        "delay": Recoil.delay
    })


@app.route('/')
def index():
    return render_template('index.html',
        enabled = Recoil.enabled,
        x = Recoil.x,
        y = Recoil.y,
        delay = Recoil.delay
    )

def makcu_loop():
    connected = Makcu.Connect()
    if connected:
        Makcu.StartButtonListener()          
        try:
            while True:
                Recoil.RecoilLoop()
                time.sleep(0.001)  
        except KeyboardInterrupt:
            print("\nShutting down...")
            Makcu.Disconnect()

def main():
    makcu_thread = threading.Thread(target=makcu_loop, daemon=True)
    makcu_thread.start()
    
    app.run(host='0.0.0.0', port=5000, debug=False)

if __name__ == "__main__":
    main()