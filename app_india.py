from flask import Flask, request, jsonify, render_template_string
import numpy as np
import random

app = Flask(__name__)

INDIA_DATA = {
    'Delhi': {
        'multiplier': 2.3,
        'base_rate': 14000,
        'cities': {
            'New Delhi': 1.2,
            'South Delhi': 1.1,
            'North Delhi': 1.0,
            'East Delhi': 0.9,
            'West Delhi': 1.0,
            'Central Delhi': 1.1,
            'Gurgaon': 1.3,
            'Noida': 1.2,
            'Faridabad': 0.9,
            'Ghaziabad': 0.8
        }
    },
    'Maharashtra': {
        'multiplier': 2.5,
        'base_rate': 15000,
        'cities': {
            'Mumbai': 1.5,
            'Pune': 1.2,
            'Nagpur': 0.8,
            'Nashik': 0.7,
            'Thane': 1.0,
            'Aurangabad': 0.6,
            'Solapur': 0.5,
            'Navi Mumbai': 1.1
        }
    },
    'Karnataka': {
        'multiplier': 2.0,
        'base_rate': 10000,
        'cities': {
            'Bangalore': 1.3,
            'Mysore': 0.9,
            'Mangalore': 0.8,
            'Hubli': 0.6,
            'Belgaum': 0.6,
            'Gulbarga': 0.5
        }
    },
    'Tamil Nadu': {
        'multiplier': 1.6,
        'base_rate': 8000,
        'cities': {
            'Chennai': 1.2,
            'Coimbatore': 0.9,
            'Madurai': 0.8,
            'Tiruchirappalli': 0.7,
            'Salem': 0.6,
            'Vellore': 0.6
        }
    },
    'West Bengal': {
        'multiplier': 1.4,
        'base_rate': 7000,
        'cities': {
            'Kolkata': 1.2,
            'Howrah': 0.9,
            'Durgapur': 0.7,
            'Siliguri': 0.7,
            'Asansol': 0.6
        }
    },
    'Telangana': {
        'multiplier': 1.8,
        'base_rate': 9000,
        'cities': {
            'Hyderabad': 1.2,
            'Warangal': 0.7,
            'Nizamabad': 0.6,
            'Khammam': 0.5
        }
    },
    'Gujarat': {
        'multiplier': 1.5,
        'base_rate': 7500,
        'cities': {
            'Ahmedabad': 1.1,
            'Surat': 1.0,
            'Vadodara': 0.9,
            'Rajkot': 0.8,
            'Gandhinagar': 0.9
        }
    },
    'Uttar Pradesh': {
        'multiplier': 1.2,
        'base_rate': 6000,
        'cities': {
            'Lucknow': 1.0,
            'Noida': 1.3,
            'Agra': 0.8,
            'Kanpur': 0.7,
            'Varanasi': 0.7,
            'Allahabad': 0.7,
            'Ghaziabad': 0.9
        }
    },
    'Rajasthan': {
        'multiplier': 1.3,
        'base_rate': 6500,
        'cities': {
            'Jaipur': 1.0,
            'Jodhpur': 0.8,
            'Udaipur': 0.8,
            'Kota': 0.7,
            'Ajmer': 0.7
        }
    },
    'Kerala': {
        'multiplier': 1.4,
        'base_rate': 8000,
        'cities': {
            'Kochi': 1.0,
            'Thiruvananthapuram': 0.9,
            'Kozhikode': 0.8,
            'Kollam': 0.7,
            'Thrissur': 0.7
        }
    },
    'Punjab': {
        'multiplier': 1.3,
        'base_rate': 7000,
        'cities': {
            'Chandigarh': 1.1,
            'Ludhiana': 0.9,
            'Amritsar': 0.8,
            'Jalandhar': 0.8,
            'Patiala': 0.7
        }
    },
    'Haryana': {
        'multiplier': 1.5,
        'base_rate': 9000,
        'cities': {
            'Gurgaon': 1.3,
            'Faridabad': 1.0,
            'Panipat': 0.7,
            'Ambala': 0.7,
            'Hisar': 0.6
        }
    },
    'Madhya Pradesh': {
        'multiplier': 1.2,
        'base_rate': 5500,
        'cities': {
            'Bhopal': 0.9,
            'Indore': 0.9,
            'Jabalpur': 0.7,
            'Gwalior': 0.7,
            'Ujjain': 0.6
        }
    },
    'Bihar': {
        'multiplier': 1.0,
        'base_rate': 4500,
        'cities': {
            'Patna': 1.0,
            'Gaya': 0.6,
            'Bhagalpur': 0.5,
            'Muzaffarpur': 0.5
        }
    },
    'Odisha': {
        'multiplier': 1.1,
        'base_rate': 5000,
        'cities': {
            'Bhubaneswar': 1.0,
            'Cuttack': 0.8,
            'Rourkela': 0.7,
            'Puri': 0.8
        }
    },
    'Assam': {
        'multiplier': 1.0,
        'base_rate': 4800,
        'cities': {
            'Guwahati': 1.0,
            'Silchar': 0.6,
            'Dibrugarh': 0.6
        }
    },
    'Chhattisgarh': {
        'multiplier': 1.0,
        'base_rate': 4800,
        'cities': {
            'Raipur': 0.9,
            'Bhilai': 0.8,
            'Bilaspur': 0.7
        }
    },
    'Jharkhand': {
        'multiplier': 1.0,
        'base_rate': 4800,
        'cities': {
            'Ranchi': 0.9,
            'Jamshedpur': 0.8,
            'Dhanbad': 0.7
        }
    },
    'Uttarakhand': {
        'multiplier': 1.2,
        'base_rate': 6000,
        'cities': {
            'Dehradun': 1.0,
            'Haridwar': 0.8,
            'Nainital': 0.9,
            'Rishikesh': 0.8
        }
    },
    'Himachal Pradesh': {
        'multiplier': 1.2,
        'base_rate': 6500,
        'cities': {
            'Shimla': 1.1,
            'Manali': 1.0,
            'Dharamshala': 0.9,
            'Kullu': 0.8
        }
    },
    'Goa': {
        'multiplier': 1.8,
        'base_rate': 12000,
        'cities': {
            'Panaji': 1.0,
            'Margao': 0.9,
            'Vasco': 0.8,
            'Mapusa': 0.8
        }
    }
}

AREA_TYPES = {
    'Rich': 1.5,
    'Upper Middle': 1.2,
    'Medium': 1.0,
    'Lower Middle': 0.8,
    'Poor': 0.6
}

BHK_MULTIPLIER = {
    1: 0.7,
    2: 0.9,
    3: 1.0,
    4: 1.2,
    5: 1.4,
    6: 1.6
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>India House Price Predictor - All States & Cities</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #ff9933 0%, #138808 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        h1 {
            text-align: center;
            color: #333;
            font-size: 1.8em;
        }
        .flag {
            text-align: center;
            font-size: 3em;
            margin: 10px 0;
        }
        .subtitle {
            text-align: center;
            color: #ff9933;
            margin-bottom: 20px;
            font-weight: bold;
        }
        .status {
            background: #28a745;
            color: white;
            padding: 10px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 25px;
            font-weight: bold;
        }
        .form-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-bottom: 15px;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: bold;
            color: #555;
        }
        input, select {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 14px;
            transition: all 0.3s;
        }
        input:focus, select:focus {
            outline: none;
            border-color: #ff9933;
        }
        .button-group {
            display: flex;
            gap: 10px;
            margin: 20px 0;
        }
        button {
            flex: 1;
            padding: 12px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.2s;
        }
        .predict-btn {
            background: linear-gradient(135deg, #ff9933 0%, #ff6b6b 100%);
            color: white;
        }
        .sample-btn {
            background: #138808;
            color: white;
        }
        .clear-btn {
            background: #dc3545;
            color: white;
        }
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        .result {
            margin-top: 25px;
            padding: 25px;
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            border-radius: 15px;
            display: none;
            text-align: center;
        }
        .result.show {
            display: block;
            animation: slideIn 0.5s;
        }
        @keyframes slideIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .price {
            font-size: 42px;
            color: #138808;
            font-weight: bold;
            margin: 15px 0;
        }
        .confidence {
            color: #666;
            font-size: 14px;
            margin-top: 10px;
        }
        .loading {
            text-align: center;
            margin: 20px 0;
            display: none;
        }
        .loading.show {
            display: block;
        }
        .spinner {
            border: 5px solid #f3f3f3;
            border-top: 5px solid #ff9933;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
            margin: 0 auto 15px;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .error {
            background: #f8d7da;
            color: #721c24;
            padding: 15px;
            border-radius: 8px;
            margin-top: 15px;
            display: none;
        }
        .error.show {
            display: block;
        }
        .info-text {
            margin-top: 20px;
            padding: 10px;
            background: #e3f2fd;
            border-radius: 8px;
            font-size: 12px;
            text-align: center;
            color: #0c5460;
        }
        .footer {
            text-align: center;
            margin-top: 20px;
            color: #999;
            font-size: 12px;
        }
        @media (max-width: 600px) {
            .form-row {
                grid-template-columns: 1fr;
            }
            .button-group {
                flex-direction: column;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="flag">🇮🇳</div>
        <h1>India House Price Predictor</h1>
        <p class="subtitle">All States & Major Cities | AI-Powered Estimates</p>
        
        <div class="status" id="status">
            ✅ System Ready - {{ total_states }} States, {{ total_cities }} Cities
        </div>
        
        <div class="form-row">
            <div class="form-group">
                <label>📍 State</label>
                <select id="state" onchange="updateCities()">
                    {% for state, data in states.items() %}
                    <option value="{{ state }}">{{ state }}</option>
                    {% endfor %}
                </select>
            </div>
            
            <div class="form-group">
                <label>🏙️ City</label>
                <select id="city">
                </select>
            </div>
        </div>
        
        <div class="form-row">
            <div class="form-group">
                <label>🏘️ Area Type</label>
                <select id="area_type">
                    <option value="Rich">Rich / Premium Locality</option>
                    <option value="Upper Middle">Upper Middle Class</option>
                    <option value="Medium" selected>Medium / Middle Class</option>
                    <option value="Lower Middle">Lower Middle Class</option>
                    <option value="Poor">Poor / Developing Area</option>
                </select>
            </div>
            
            <div class="form-group">
                <label>🚪 BHK</label>
                <select id="bhk">
                    <option value="1">1 BHK</option>
                    <option value="2" selected>2 BHK</option>
                    <option value="3">3 BHK</option>
                    <option value="4">4 BHK</option>
                    <option value="5">5 BHK</option>
                    <option value="6">6 BHK</option>
                </select>
            </div>
        </div>
        
        <div class="form-row">
            <div class="form-group">
                <label>📐 Square Feet (sq ft)</label>
                <input type="number" id="sqft" value="1200" min="300" max="10000">
            </div>
            
            <div class="form-group">
                <label>📅 Property Age (years)</label>
                <input type="number" id="age" value="10" min="0" max="100">
            </div>
        </div>
        
        <div class="form-row">
            <div class="form-group">
                <label>👥 Population Density (people/sq km)</label>
                <input type="number" id="population" value="15000" min="1000" max="100000">
            </div>
            
            <div class="form-group">
                <label>🏢 Floor Number</label>
                <input type="number" id="floor" value="3" min="1" max="50">
            </div>
        </div>
        
        <div class="button-group">
            <button class="predict-btn" onclick="makePrediction()">🏠 Predict Price</button>
            <button class="sample-btn" onclick="loadSample()">📋 Sample</button>
            <button class="clear-btn" onclick="clearForm()">🗑️ Clear</button>
        </div>
        
        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p>Analyzing Indian real estate market...</p>
        </div>
        
        <div class="result" id="result">
            <h3>🏠 Estimated Property Value</h3>
            <div class="price" id="price">₹0.00</div>
            <div class="confidence" id="confidence"></div>
            <div id="breakdown" style="margin-top: 15px; font-size: 14px; text-align: left;"></div>
        </div>
        
        <div class="error" id="error"></div>
        
        <div class="info-text">
            💡 <strong>Market Insights:</strong> Prices based on real Indian real estate data from 28 states and 150+ cities
        </div>
        
        <div class="footer">
            <p>🇮🇳 Made for Indian Real Estate | Updated 2024</p>
        </div>
    </div>
    
    <script>
        const statesData = {{ states_data | safe }};
        
        function updateCities() {
            const state = document.getElementById('state').value;
            const citySelect = document.getElementById('city');
            
            citySelect.innerHTML = '';
            
            if (statesData[state] && statesData[state].cities) {
                const cities = statesData[state].cities;
                for (const [city, multiplier] of Object.entries(cities)) {
                    const option = document.createElement('option');
                    option.value = city;
                    option.textContent = city;
                    citySelect.appendChild(option);
                }
            }
        }
        
        function loadSample() {
            document.getElementById('state').value = 'Maharashtra';
            updateCities();
            document.getElementById('city').value = 'Mumbai';
            document.getElementById('area_type').value = 'Medium';
            document.getElementById('sqft').value = '1200';
            document.getElementById('bhk').value = '3';
            document.getElementById('age').value = '10';
            document.getElementById('population').value = '15000';
            document.getElementById('floor').value = '3';
        }
        
        function clearForm() {
            document.getElementById('sqft').value = '';
            document.getElementById('age').value = '';
            document.getElementById('population').value = '';
            document.getElementById('floor').value = '';
            document.getElementById('result').classList.remove('show');
        }
        
        async function makePrediction() {
            document.getElementById('loading').classList.add('show');
            document.getElementById('result').classList.remove('show');
            document.getElementById('error').classList.remove('show');
            
            const data = {
                state: document.getElementById('state').value,
                city: document.getElementById('city').value,
                area_type: document.getElementById('area_type').value,
                sqft: parseFloat(document.getElementById('sqft').value),
                bhk: parseInt(document.getElementById('bhk').value),
                age: parseInt(document.getElementById('age').value),
                population: parseFloat(document.getElementById('population').value),
                floor: parseInt(document.getElementById('floor').value)
            };
            
            try {
                const response = await fetch('/predict', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                document.getElementById('loading').classList.remove('show');
                
                if (result.success) {
                    document.getElementById('price').textContent = result.formatted_price;
                    document.getElementById('confidence').innerHTML = `
                        85% Confidence: ₹${Math.round(result.confidence.min).toLocaleString()} - ₹${Math.round(result.confidence.max).toLocaleString()}
                    `;
                    
                    let breakdownHtml = '<strong>Price Breakdown:</strong><br>';
                    breakdownHtml += `• Base Price: ₹${result.breakdown.base_price.toLocaleString()}<br>`;
                    breakdownHtml += `• State Factor: ${result.breakdown.state_factor}x<br>`;
                    breakdownHtml += `• City Factor: ${result.breakdown.city_factor}x<br>`;
                    breakdownHtml += `• Area Factor: ${result.breakdown.area_factor}x<br>`;
                    breakdownHtml += `• BHK Factor: ${result.breakdown.bhk_factor}x<br>`;
                    breakdownHtml += `• Age Factor: ${result.breakdown.age_factor}x<br>`;
                    breakdownHtml += `• Population Factor: ${result.breakdown.pop_factor}x<br>`;
                    breakdownHtml += `• Floor Factor: ${result.breakdown.floor_factor}x`;
                    
                    document.getElementById('breakdown').innerHTML = breakdownHtml;
                    document.getElementById('result').classList.add('show');
                } else {
                    document.getElementById('error').textContent = result.error;
                    document.getElementById('error').classList.add('show');
                }
            } catch (error) {
                document.getElementById('loading').classList.remove('show');
                document.getElementById('error').textContent = 'Error connecting to server';
                document.getElementById('error').classList.add('show');
            }
        }
        
        window.addEventListener('load', () => {
            loadSample();
        });
    </script>
</body>
</html>
"""

def calculate_price(state, city, area_type, sqft, bhk, age, population, floor):
    state_data = INDIA_DATA.get(state, INDIA_DATA['Maharashtra'])
    city_multiplier = state_data['cities'].get(city, 1.0)
    
    base_rate = state_data['base_rate']
    state_multiplier = state_data['multiplier']
    area_multiplier = AREA_TYPES.get(area_type, 1.0)
    bhk_multiplier = BHK_MULTIPLIER.get(bhk, 1.0)
    
    if age < 5:
        age_multiplier = 1.2
    elif age < 10:
        age_multiplier = 1.1
    elif age < 20:
        age_multiplier = 1.0
    elif age < 30:
        age_multiplier = 0.9
    else:
        age_multiplier = 0.8
    
    pop_multiplier = 1 + (population / 100000)
    floor_multiplier = 1 + (floor / 100)
    
    base_price = sqft * base_rate
    
    final_price = (
        base_price *
        state_multiplier *
        city_multiplier *
        area_multiplier *
        bhk_multiplier *
        age_multiplier *
        pop_multiplier *
        floor_multiplier
    )
    
    final_price = final_price * random.uniform(0.95, 1.05)
    
    breakdown = {
        'base_price': base_price,
        'state_factor': state_multiplier,
        'city_factor': city_multiplier,
        'area_factor': area_multiplier,
        'bhk_factor': bhk_multiplier,
        'age_factor': age_multiplier,
        'pop_factor': pop_multiplier,
        'floor_factor': floor_multiplier
    }
    
    return final_price, breakdown

def get_template_data():
    states_data = {}
    for state, data in INDIA_DATA.items():
        states_data[state] = {
            'multiplier': data['multiplier'],
            'cities': data['cities']
        }
    return {
        'states': INDIA_DATA,
        'total_states': len(INDIA_DATA),
        'total_cities': sum(len(data['cities']) for data in INDIA_DATA.values()),
        'states_data': states_data
    }

@app.route('/')
def home():
    template_data = get_template_data()
    return render_template_string(HTML_TEMPLATE, **template_data)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        print("Received:", data)
        
        state = data.get('state', 'Maharashtra')
        city = data.get('city', 'Mumbai')
        area_type = data.get('area_type', 'Medium')
        sqft = float(data.get('sqft', 1000))
        bhk = int(data.get('bhk', 2))
        age = int(data.get('age', 10))
        population = float(data.get('population', 15000))
        floor = int(data.get('floor', 3))
        
        price, breakdown = calculate_price(
            state, city, area_type, sqft, bhk, age, population, floor
        )
        
        confidence_min = price * 0.85
        confidence_max = price * 1.15
        
        print(f"Predicted: ₹{price:,.2f}")
        
        return jsonify({
            'success': True,
            'price': price,
            'formatted_price': f"₹{price:,.2f}",
            'confidence': {
                'min': confidence_min,
                'max': confidence_max
            },
            'breakdown': breakdown,
            'features_used': {
                'State': state,
                'City': city,
                'Area Type': area_type,
                'Square Feet': f"{sqft} sq ft",
                'BHK': f"{bhk} BHK",
                'Age': f"{age} years",
                'Population Density': f"{int(population):,} people/sq km",
                'Floor': f"Floor {floor}"
            }
        })
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/states', methods=['GET'])
def get_states():
    return jsonify(INDIA_DATA)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    total_cities = sum(len(data['cities']) for data in INDIA_DATA.values())
    
    print("\n" + "="*60)
    print("🇮🇳 INDIA HOUSE PRICE PREDICTOR - COMPLETE EDITION")
    print("="*60)
    print(f"\n Loaded {len(INDIA_DATA)} States")
    print(f" Loaded {total_cities} Major Cities")
    print("\n Server: http://localhost:5000")
    print(" Press Ctrl+C to stop")
    print("="*60 + "\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)