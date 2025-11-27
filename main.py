from Makcu.makcu import Makcu
from Recoil.recoil import Recoil

from flask import Flask, render_template, request, jsonify
import time
import threading

app = Flask(__name__)

@app.route('/update', methods=['POST'])
def update():
    data = request.get_json()

    Recoil.mode = str(data.get("mode", Recoil.mode))
    Recoil.enabled = bool(data.get("enabled", Recoil.enabled))
    Recoil.x = float(data.get("x", Recoil.x))
    Recoil.y = float(data.get("y", Recoil.y))
    Recoil.delay = float(data.get("delay", Recoil.delay))

    return jsonify({
        "status": "success",
        "mode": Recoil.mode,
        "enabled": Recoil.enabled,
        "x": Recoil.x,
        "y": Recoil.y,
        "delay": Recoil.delay
    })

@app.route('/update_pattern', methods=['POST'])
def update_pattern():
    data = request.get_json()
    
    Recoil.pattern_enabled = bool(data.get("pattern_enabled", Recoil.pattern_enabled))
    
    # Parse pattern from list of objects [{x: 0, y: 3}, {x: 1, y: 3}, ...]
    pattern_data = data.get("pattern", [])
    Recoil.pattern = [(float(item['x']), float(item['y'])) for item in pattern_data]
    
    return jsonify({
        "status": "success",
        "pattern_enabled": Recoil.pattern_enabled,
        "pattern": [{"x": x, "y": y} for x, y in Recoil.pattern]
    })

@app.route('/get_pattern', methods=['GET'])
def get_pattern():
    return jsonify({
        "pattern_enabled": Recoil.pattern_enabled,
        "pattern": [{"x": x, "y": y} for x, y in Recoil.pattern]
    })

@app.route('/')
def index():
    return render_template('index.html',
        mode = Recoil.mode,
        enabled = Recoil.enabled,
        x = Recoil.x,
        y = Recoil.y,
        delay = Recoil.delay,
        pattern_enabled = Recoil.pattern_enabled,
        pattern = [{"x": x, "y": y} for x, y in Recoil.pattern]
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