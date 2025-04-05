# app.py
from flask import Flask, render_template, request, jsonify
import json
import os
import random
from mock.sap_mock import SAPMockGenerator
from genai.factors import InvestmentFactorsCalculator
from genai.recommendation import InvestmentRecommendationEngine

app = Flask(__name__)

# Initialize and generate mock data if not exists
data_dir = os.path.join(os.path.dirname(__file__), 'data')
if not os.path.exists(os.path.join(data_dir, 'clients.json')):
    generator = SAPMockGenerator()
    generator.generate_clients(100)
    generator.generate_portfolios()
    generator.generate_market_trends()
    generator.export_to_json(data_dir)

# Load mock data
with open(os.path.join(data_dir, 'clients.json')) as f:
    clients = json.load(f)

with open(os.path.join(data_dir, 'portfolios.json')) as f:
    portfolios = json.load(f)

with open(os.path.join(data_dir, 'market.json')) as f:
    market_trends = json.load(f)

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html', 
                          clients=clients[:10],
                          market_trends=market_trends)

@app.route('/advice/<client_id>')
def advice_page(client_id):
    """Investment advice page for a specific client"""
    client = next((c for c in clients if c['client_id'] == client_id), None)
    if not client:
        return "Client not found", 404
        
    return render_template('advice.html', 
                          client=client,
                          clients=clients)

@app.route('/api/advice/<client_id>')
def get_advice(client_id):
    """API endpoint to get personalized investment advice"""
    client = next((c for c in clients if c['client_id'] == client_id), None)
    portfolio = next((p for p in portfolios if p['client_id'] == client_id), None)
    
    if not client or not portfolio:
        return jsonify({"error": "Client not found"}), 404
    
    # Calculate investment factors
    factors_calc = InvestmentFactorsCalculator(client, portfolio, market_trends)
    factors = factors_calc.calculate_all_factors()
    
    # Generate recommendations
    engine = InvestmentRecommendationEngine(client, portfolio, market_trends, factors)
    advice = engine.generate_recommendations()
    
    return jsonify(advice)

@app.route('/api/clients')
def get_clients():
    """API endpoint to get client list"""
    return jsonify(clients)

if __name__ == '__main__':
    app.run(debug=True)

