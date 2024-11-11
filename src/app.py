from flask import Flask, request, jsonify
from src.models import PowerPlant, Fuels
from src.optimizer import calculate_production_plan

app = Flask(__name__)

@app.route('/productionplan', methods=['POST'])
def production_plan():
    try:
        payload = request.get_json()
        if not payload:
            return jsonify({"error": "No input data provided"}), 400

        # Create and validate fuels object
        try:
            fuels = Fuels(
                gas=payload['fuels']['gas(euro/MWh)'],
                kerosine=payload['fuels']['kerosine(euro/MWh)'],
                co2=payload['fuels']['co2(euro/ton)'],
                wind=payload['fuels']['wind(%)']
            )
        except KeyError as e:
            return jsonify({"error": f"Missing fuel data: {str(e)}"}), 400

        # Create powerplants list
        try:
            powerplants = [
                PowerPlant(
                    name=p['name'],
                    type=p['type'],
                    efficiency=p['efficiency'],
                    pmin=p['pmin'],
                    pmax=p['pmax']
                ) for p in payload['powerplants']
            ]
        except KeyError as e:
            return jsonify({"error": f"Missing powerplant data: {str(e)}"}), 400

        # Calculate production plan
        result = calculate_production_plan(payload['load'], fuels, powerplants)
        response = [{"name": output.name, "p": output.p} for output in result]
        
        return jsonify(response)
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)


