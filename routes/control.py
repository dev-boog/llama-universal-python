from flask import Blueprint, request, jsonify
from Recoil.recoil import Recoil

control_bp = Blueprint('control', __name__)

# Live update recoilc control settings
@control_bp.route('/update', methods=['POST'])
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
