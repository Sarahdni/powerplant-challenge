----------------------------------------------
# POWERPLANT CODING CHALLENGE
----------------------------------------------
A REST API that helps determine the most cost-effective production plan for powerplants to meet the load demand while respecting the constraints of each powerplant.

---------------------------------------------
## SETUP
---------------------------------------------
### Local Setup

1. Create virtual environment
```bash
python -m venv venv 
```

2. Activate virtual environment
```bash
source venv/bin/activate  # MacOS/Linux 
or
.\venv\Scripts\activate   # Windows
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Run the application
```bash
python src/app.py
```

The API will be running on http://localhost:8888

### Docker Setup

1. Build the image
```bash
docker build -t powerplant-challenge .
```

2. Run the container
```bash
docker run -p 8888:8888 powerplant-challenge
```


----------------------------------------------
## API DOCUMENTATION
----------------------------------------------

### Endpoint: `POST /productionplan`

Calculates the optimal power production plan based on:
- Load demand
- Fuel prices (gas, kerosine, co2)
- Wind percentage
- Each powerplant's specifications (min/max capacity, efficiency)

### Request Format
```json
{
  "load": 910,
  "fuels":
  {
    "gas(euro/MWh)": 13.4,
    "kerosine(euro/MWh)": 50.8,
    "co2(euro/ton)": 20,
    "wind(%)": 60
  },
  "powerplants": [
    {
      "name": "gasfiredbig1",
      "type": "gasfired",
      "efficiency": 0.53,
      "pmin": 100,
      "pmax": 460
    },
    // ... other powerplants
  ]
}
```

### Reponse Format
```json
[
    {
        "name": "windpark1",
        "p": 90.0
    },
    {
        "name": "windpark2",
        "p": 21.6
    },
    {
        "name": "gasfiredbig1",
        "p": 460.0
    },
    {
        "name": "gasfiredbig2",
        "p": 338.4
    },
    {
        "name": "gasfiredsomewhatsmaller",
        "p": 0.0
    },
    {
        "name": "tj1",
        "p": 0.0
    }
]
```

### Example Usage
```bash
curl -s -X POST \
  http://localhost:8888/productionplan \
  -H "Content-Type: application/json" \
  -d @payloads/payload1.json | jq . 
```


### Testing
Run tests using pytest

Test payloads are available in the payloads/ directory.

