import logging
from flask import Flask, request, jsonify
from models import PowerPlant, Fuels, PowerPlantOutput
from optimizer import calculate_production_plan

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/productionplan', methods=['POST'])
def production_plan():
    """
    Process production plan request and return optimal power distribution.

    Expected JSON payload:
        {
            "load": float,            # Required power in MW
            "fuels": {
                "gas(euro/MWh)": float,
                "kerosine(euro/MWh)": float,
                "co2(euro/ton)": float,
                "wind(%)": float
            },
            "powerplants": [
                {
                    "name": str,
                    "type": str,      # "gasfired", "turbojet", or "windturbine"
                    "efficiency": float,
                    "pmin": float,    # Minimum power in MW
                    "pmax": float     # Maximum power in MW
                },
                ...
            ]
        }

    Returns:
        200: List of power allocations
        400: Invalid input data
        422: Cannot meet load requirement
        500: Server error
    """
    try:
        payload = request.get_json()
        if not payload:
            return jsonify({"error": "No input data provided"}), 400

        # Validate load
        load = payload.get('load', 0)
        if load <= 0:
            return jsonify({"error": "Load must be positive"}), 400

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

        if not fuels.validate():
            return jsonify({"error": "Invalid fuels data"}), 400

        # Create and validate powerplants
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

        if not all(p.validate() for p in powerplants):
            return jsonify({"error": "Invalid powerplant data"}), 400

        # Calculate production plan
        try:
            result = calculate_production_plan(load, fuels, powerplants)
            response = [{"name": output.name, "p": output.p} for output in result]
            logger.info(f"Successfully calculated production plan for load: {load}")
            return jsonify(response)

        except ValueError as e:
            logger.error(f"Optimization error: {str(e)}")
            return jsonify({"error": str(e)}), 422
            
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    port = 8888
    logger.info(f"Starting server on port {port}")
    app.run(host='0.0.0.0', port=port)