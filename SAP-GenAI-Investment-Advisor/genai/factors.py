# genai/factors.py
import random
import numpy as np

class InvestmentFactorsCalculator:
    """
    Calculates investment factors that influence investment recommendations
    similar to the pricing factors shown in the SAP GenAI Dynamic Pricing Engine
    """
    
    def __init__(self, client, portfolio, market_trends):
        self.client = client
        self.portfolio = portfolio
        self.market_trends = market_trends
        
    def calculate_market_trend_factor(self):
        """
        Calculates how current market trends should influence investment decisions
        > 1: Positive market trends suggest more aggressive investing
        < 1: Negative market trends suggest more conservative positioning
        """
        # Get overall market growth
        overall_growth = self.market_trends["overall_market"]["growth"]
        
        # Normalize to a factor around 1.0
        factor = 1.0 + overall_growth * 2
        
        # Add some randomness for realistic variation
        factor = factor * random.uniform(0.95, 1.05)
        
        # Ensure within reasonable bounds
        return round(max(min(factor, 1.25), 0.75), 2)
    
    def calculate_risk_tolerance_factor(self):
        """
        Adjusts recommendations based on client's risk tolerance
        > 1: Higher risk tolerance allows for more aggressive recommendations
        < 1: Lower risk tolerance requires more conservative recommendations
        """
        risk_mapping = {
            "Conservative": 0.85,
            "Moderate": 1.0,
            "Growth": 1.1,
            "Aggressive": 1.2
        }
        
        base_factor = risk_mapping[self.client["risk_tolerance"]]
        
        # Adjust for age (older clients get more conservative recommendations)
        age_adjustment = max(0, (60 - self.client["age"]) / 100)
        
        # Final factor
        factor = base_factor + age_adjustment
        
        # Add slight randomness
        factor = factor * random.uniform(0.98, 1.02)
        
        return round(factor, 2)
    
    def calculate_portfolio_diversification_factor(self):
        """
        Evaluates current portfolio diversification level
        < 1: Poor diversification suggests rebalancing
        = 1: Well-diversified portfolio
        """
        # Count asset classes
        num_assets = len(self.portfolio["holdings"])
        
        # Calculate allocation concentration (higher is less diversified)
        allocations = [h["current_allocation"] for h in self.portfolio["holdings"]]
        concentration = np.std(allocations) / np.mean(allocations) if allocations else 1.0
        
        # Base factor on diversification metrics
        if num_assets <= 3:
            base_factor = 0.85  # Poorly diversified
        elif num_assets <= 5:
            base_factor = 0.9
        elif num_assets <= 8:
            base_factor = 0.95
        else:
            base_factor = 1.0  # Well diversified
            
        # Adjust for concentration
        concentration_adj = max(0, 0.1 - (concentration * 0.05))
        
        factor = base_factor + concentration_adj
        
        return round(factor, 2)
    
    def calculate_age_based_allocation_factor(self):
        """
        Determines if current allocation is appropriate for client's age
        > 1: Allocation can be more aggressive
        < 1: Allocation should be more conservative
        """
        age = self.client["age"]
        
        # Simple age-based stock allocation rule: 100 - age
        target_stock_allocation = max(100 - age, 20) / 100
        
        # Estimate current stock allocation (simplified)
        stock_assets = ["Large Cap Stocks", "Mid Cap Stocks", "Small Cap Stocks", 
                        "International Developed", "Emerging Markets"]
        
        current_stock_allocation = sum(h["current_allocation"] for h in self.portfolio["holdings"] 
                                     if h["asset_class"] in stock_assets) / 100
        
        # Calculate factor based on difference
        difference = target_stock_allocation - current_stock_allocation
        factor = 1.0 + difference
        
        return round(factor, 2)
    
    def calculate_goal_alignment_factor(self):
        """
        Measures how well current portfolio aligns with financial goals
        > 1: Portfolio well-aligned with goals, continue strategy
        < 1: Portfolio misaligned with goals, adjust strategy
        """
        goal = self.client["financial_goal"]
        time_horizon = self.client["time_horizon"]
        
        # Baseline factor
        factor = 1.0
        
        # Goal-specific adjustments
        if goal == "Retirement" and time_horizon > 15:
            factor += 0.15  # Long-term retirement goals align with growth
        elif goal == "Education" and time_horizon < 5:
            factor -= 0.1   # Short-term education needs need conservative approach
        elif goal == "Home Purchase" and time_horizon < 3:
            factor -= 0.15  # Very short-term goals need capital preservation
        elif goal == "Wealth Growth":
            factor += 0.1   # Growth goals align with aggressive strategies
        
        # Add randomness
        factor = factor * random.uniform(0.95, 1.05)
        
        return round(factor, 2)
    
    def calculate_all_factors(self):
        """Calculate all investment factors"""
        return {
            "market_trend_factor": self.calculate_market_trend_factor(),
            "risk_tolerance_factor": self.calculate_risk_tolerance_factor(),
            "portfolio_diversification_factor": self.calculate_portfolio_diversification_factor(),
            "age_based_allocation_factor": self.calculate_age_based_allocation_factor(), 
            "goal_alignment_factor": self.calculate_goal_alignment_factor()
        }

