from Makcu.makcu import Makcu
from Recoil.recoil import Recoil

from flask import Flask, render_template, request, jsonify
import time
import threading
import json
import os

app = Flask(__name__)
PATTERN_FILE = "SavedPatterns.json"

# Save current pattern to file
@app.route('/save_pattern', methods=['POST'])
def save_pattern():
    data = request.get_json()
    pattern_name = data.get("name", "default")

    if os.path.exists(PATTERN_FILE):
        with open(PATTERN_FILE, "r") as f:
            saved_patterns = json.load(f)
    else:
        saved_patterns = {}

    saved_patterns[pattern_name] = [{"x": x, "y": y} for x, y in Recoil.pattern]

    with open(PATTERN_FILE, "w") as f:
        json.dump(saved_patterns, f, indent=4)

    return jsonify({"status": "success", "saved_pattern": pattern_name})


@app.route('/load_pattern', methods=['POST'])
def load_pattern():
    data = request.get_json()
    pattern_name = data.get("name", "default")

    if not os.path.exists(PATTERN_FILE):
        return jsonify({"status": "error", "message": "No saved patterns found"}), 404

    with open(PATTERN_FILE, "r") as f:
        saved_patterns = json.load(f)

    if pattern_name not in saved_patterns:
        return jsonify({"status": "error", "message": "Pattern not found"}), 404

    Recoil.pattern = [(item['x'], item['y']) for item in saved_patterns[pattern_name]]
    Recoil.pattern_enabled = True

    return jsonify({"status": "success", "pattern": saved_patterns[pattern_name]})

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