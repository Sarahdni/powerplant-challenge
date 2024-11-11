from flask import Flask, request, jsonify
from src.models import PowerPlant, Fuels

app = Flask(__name__)

@app.route('/productionplan', methods=['POST'])
def production_plan():
    try:
        payload = request.get_json()
        if not payload:
            return jsonify({"error": "No input data provided"}), 400
            
        # Basic response for now
        return jsonify([{"name": "gasfiredbig1", "p": 0}])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)