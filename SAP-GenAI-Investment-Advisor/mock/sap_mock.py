# mock/sap_mock.py
import os
import json
import random
from faker import Faker
fake = Faker()

class SAPMockGenerator:
    def __init__(self):
        self.clients = []
        self.portfolios = []
        self.market_trends = {}
    
    def generate_clients(self, count=100):
        """Generate mock client profiles"""
        self.clients = []
        risk_profiles = ["Conservative", "Moderate", "Growth", "Aggressive"]
        financial_goals = ["Retirement", "Education", "Wealth Growth", "Short-term Savings", 
                          "Home Purchase", "Business Investment", "Legacy Planning"]
        
        for i in range(count):
            age = random.randint(25, 75)
            # Slightly bias risk tolerance based on age
            risk_weights = [0.4, 0.3, 0.2, 0.1] if age > 55 else [0.1, 0.3, 0.4, 0.2]
            risk_tolerance = random.choices(risk_profiles, weights=risk_weights)[0]
            
            client = {
                "client_id": f"CLIENT{i+1:04d}",
                "name": fake.name(),
                "email": fake.email(),
                "age": age,
                "income": round(random.uniform(50000, 500000), -3),
                "risk_tolerance": risk_tolerance,
                "financial_goal": random.choice(financial_goals),
                "time_horizon": random.randint(1, 30),
                "investment_experience": random.choice(["None", "Limited", "Moderate", "Extensive"]),
                "last_consultation": fake.date_between(start_date="-1y", end_date="today").strftime("%Y-%m-%d")
            }
            self.clients.append(client)
        return self.clients
    
    def generate_portfolios(self):
        """Generate mock portfolio data for each client"""
        self.portfolios = []
        asset_classes = [
            "Large Cap Stocks", "Mid Cap Stocks", "Small Cap Stocks", 
            "International Developed", "Emerging Markets", "Real Estate", 
            "Corporate Bonds", "Government Bonds", "High Yield Bonds",
            "Commodities", "Cash"
        ]
        
        for client in self.clients:
            # Portfolio size based on age and risk tolerance
            portfolio_base = random.uniform(50000, 2000000)
            if client["risk_tolerance"] == "Aggressive":
                asset_count = random.randint(5, 11)
                stock_weight = 0.8
            elif client["risk_tolerance"] == "Growth":
                asset_count = random.randint(4, 9)
                stock_weight = 0.7
            elif client["risk_tolerance"] == "Moderate":
                asset_count = random.randint(4, 8)
                stock_weight = 0.6
            else:  # Conservative
                asset_count = random.randint(3, 7)
                stock_weight = 0.4
            
            # Select asset classes for this portfolio
            selected_assets = random.sample(asset_classes, asset_count)
            
            # Allocate weights
            weights = [random.random() for _ in range(asset_count)]
            total_weight = sum(weights)
            weights = [w/total_weight for w in weights]
            
            holdings = []
            total_value = 0
            for i, asset in enumerate(selected_assets):
                value = round(portfolio_base * weights[i], 2)
                total_value += value
                purchase_date = fake.date_between(start_date="-5y", end_date="-1m").strftime("%Y-%m-%d")
                
                holdings.append({
                    "asset_class": asset,
                    "value": value,
                    "purchase_date": purchase_date,
                    "current_allocation": round(weights[i] * 100, 2),
                    "performance_ytd": round(random.uniform(-0.15, 0.25), 4)
                })
            
            portfolio = {
                "client_id": client["client_id"],
                "total_value": round(total_value, 2),
                "holdings": holdings
            }
            self.portfolios.append(portfolio)
        return self.portfolios
    
    def generate_market_trends(self):
        """Generate mock market trends and forecasts"""
        sectors = [
            "Technology", "Healthcare", "Financials", "Consumer Discretionary", 
            "Consumer Staples", "Energy", "Materials", "Industrials", 
            "Utilities", "Real Estate", "Communication Services"
        ]
        
        trends = []
        for sector in sectors:
            # Generate current trend
            growth = round(random.uniform(-0.08, 0.25), 4)
            
            # Generate 6-month forecast (somewhat correlated with current trend)
            forecast_base = growth * 0.7 + random.uniform(-0.05, 0.05)
            forecast = round(min(max(forecast_base, -0.15), 0.3), 4)
            
            # Generate volatility measure
            volatility = round(random.uniform(0.05, 0.45), 4)
            
            trends.append({
                "sector": sector,
                "current_growth": growth,
                "forecast_growth": forecast,
                "volatility": volatility,
                "analyst_sentiment": random.choice(["Bearish", "Neutral", "Bullish", "Strongly Bullish"])
            })
        
        # Add overall market trend
        overall_growth = round(sum(t["current_growth"] for t in trends) / len(trends), 4)
        
        self.market_trends = {
            "trends": trends,
            "overall_market": {
                "growth": overall_growth,
                "volatility_index": round(random.uniform(10, 35), 2),
                "interest_rate": round(random.uniform(0.5, 6.0), 2),
                "inflation_rate": round(random.uniform(1.0, 8.0), 2)
            }
        }
        return self.market_trends
    
    def export_to_json(self, base_path="data"):
        """Export all generated data to JSON files"""
        if not os.path.exists(base_path):
            os.makedirs(base_path)
            
        with open(f"{base_path}/clients.json", "w") as f:
            json.dump(self.clients, f, indent=2)
        
        with open(f"{base_path}/portfolios.json", "w") as f:
            json.dump(self.portfolios, f, indent=2)
        
        with open(f"{base_path}/market.json", "w") as f:
            json.dump(self.market_trends, f, indent=2)

# For standalone execution
if __name__ == "__main__":
    import os
    generator = SAPMockGenerator()
    generator.generate_clients(100)
    generator.generate_portfolios()
    generator.generate_market_trends()
    generator.export_to_json()
    print("Mock data generated successfully!")

