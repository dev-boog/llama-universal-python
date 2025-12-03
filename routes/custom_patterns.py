from flask import Blueprint, request, jsonify
import json
import os
from Recoil.recoil import Recoil

patterns_bp = Blueprint('patterns', __name__)
PATTERN_FILE = "SavedPatterns.json"

# Save the current created pattern to SavedPatterns.json
@patterns_bp.route('/save_pattern', methods=['POST'])
def save_pattern():
    data = request.get_json()
    name = data.get("name", "default")

    saved = {}
    if os.path.exists(PATTERN_FILE):
        with open(PATTERN_FILE) as f:
            saved = json.load(f)

    saved[name] = [{"x": x, "y": y} for x, y in Recoil.pattern]

    with open(PATTERN_FILE, "w") as f:
        json.dump(saved, f, indent=4)

    return jsonify({"status": "success", "saved_pattern": name})


# Load a saved pattern from SavedPatterns.json
@patterns_bp.route('/load_pattern', methods=['POST'])
def load_pattern():
    data = request.get_json()
    name = data.get("name", "default")

    if not os.path.exists(PATTERN_FILE):
        return jsonify({"status": "error", "message": "No patterns saved"}), 404

    with open(PATTERN_FILE) as f:
        saved = json.load(f)

    if name not in saved:
        return jsonify({"status": "error", "message": "Pattern not found"}), 404

    Recoil.pattern = [(p['x'], p['y']) for p in saved[name]]
    Recoil.pattern_enabled = True

    return jsonify({"status": "success", "pattern": saved[name]})


# Update the recoil custom pattern settings
@patterns_bp.route('/update_pattern', methods=['POST'])
def update_pattern():
    data = request.get_json()
    
    Recoil.pattern_enabled = bool(data.get("pattern_enabled", Recoil.pattern_enabled))
    pattern_data = data.get("pattern", [])
    Recoil.pattern = [(float(p['x']), float(p['y'])) for p in pattern_data]
    
    return jsonify({
        "status": "success",
        "pattern_enabled": Recoil.pattern_enabled,
        "pattern": [{"x": x, "y": y} for x, y in Recoil.pattern]
    })

# Get the current recoil custom pattern settings
@patterns_bp.route('/get_pattern', methods=['GET'])
def get_pattern():
    return jsonify({
        "pattern_enabled": Recoil.pattern_enabled,
        "pattern": [{"x": x, "y": y} for x, y in Recoil.pattern]
    })