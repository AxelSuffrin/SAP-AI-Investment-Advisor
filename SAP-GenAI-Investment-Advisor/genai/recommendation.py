# genai/recommendation.py
import random
from datetime import datetime

class InvestmentRecommendationEngine:
    """
    Simulates a Generative AI recommendation engine that would
    typically be implemented using SAP's Generative AI Hub
    """
    
    def __init__(self, client, portfolio, market_trends, factors):
        self.client = client
        self.portfolio = portfolio
        self.market_trends = market_trends
        self.factors = factors
        
    def _get_sector_outlook(self, asset_class):
        """Map asset classes to market sectors and get outlook"""
        # Simplified mapping of asset classes to sectors
        mapping = {
            "Large Cap Stocks": ["Technology", "Financials", "Healthcare"],
            "Mid Cap Stocks": ["Industrials", "Consumer Discretionary"],
            "Small Cap Stocks": ["Consumer Discretionary", "Materials"],
            "International Developed": ["Financials", "Industrials", "Consumer Staples"],
            "Emerging Markets": ["Technology", "Materials", "Energy"],
            "Real Estate": ["Real Estate"],
            "Corporate Bonds": ["Financials"],
            "Government Bonds": ["Financials"],
            "High Yield Bonds": ["Financials"],
            "Commodities": ["Materials", "Energy"],
            "Cash": []
        }
        
        if asset_class not in mapping or not mapping[asset_class]:
            return 0
            
        # Get average growth for related sectors
        sectors = mapping[asset_class]
        sector_trends = [t for t in self.market_trends["trends"] if t["sector"] in sectors]
        
        if not sector_trends:
            return 0
            
        avg_growth = sum(t["forecast_growth"] for t in sector_trends) / len(sector_trends)
        return avg_growth
    
    def _calculate_recommendation_score(self, holding):
        """Calculate a recommendation score for a specific holding"""
        # Get sector outlook
        sector_outlook = self._get_sector_outlook(holding["asset_class"])
        
        # Base score on sector outlook and asset performance
        base_score = sector_outlook * 5 + holding["performance_ytd"] * 3
        
        # Apply factor weights
        market_weight = self.factors["market_trend_factor"] * 0.2
        risk_weight = self.factors["risk_tolerance_factor"] * 0.25
        diversification_weight = self.factors["portfolio_diversification_factor"] * 0.15
        age_weight = self.factors["age_based_allocation_factor"] * 0.15
        goal_weight = self.factors["goal_alignment_factor"] * 0.25
        
        # Calculate final score
        factor_modifier = (market_weight + risk_weight + diversification_weight + 
                          age_weight + goal_weight) / 1.0
        
        final_score = base_score * factor_modifier
        
        # Add some randomness for realistic variation
        final_score = final_score * random.uniform(0.9, 1.1)
        
        return final_score
    
    def _get_recommendation_action(self, score, current_allocation):
        """Determine recommendation action based on score"""
        if score > 0.5:
            return "Increase Allocation" if current_allocation < 25 else "Hold"
        elif score > 0:
            return "Hold"
        elif score > -0.5:
            return "Reduce Allocation" if current_allocation > 15 else "Hold"
        else:
            return "Sell"
    
    def _get_allocation_change(self, action, current_allocation):
        """Determine suggested allocation change"""
        if action == "Increase Allocation":
            return min(5, 25 - current_allocation)
        elif action == "Reduce Allocation":
            return max(-5, -(current_allocation - 5))
        else:
            return 0
    
    def _generate_explanation(self, holding, action, score, sector_outlook):
        """Generate natural language explanation for the recommendation"""
        asset_class = holding["asset_class"]
        performance = holding["performance_ytd"]
        
        explanations = []
        
        # Market trend factor explanation
        if self.factors["market_trend_factor"] > 1.05:
            explanations.append(f"Positive market trends indicate favorable conditions for {asset_class}.")
        elif self.factors["market_trend_factor"] < 0.95:
            explanations.append(f"Current market volatility suggests caution with {asset_class} positions.")
        
        # Risk tolerance explanation
        if self.factors["risk_tolerance_factor"] > 1.05 and action == "Increase Allocation":
            explanations.append(f"Your {self.client['risk_tolerance'].lower()} risk profile supports increased exposure to {asset_class}.")
        elif self.factors["risk_tolerance_factor"] < 0.95 and action == "Reduce Allocation":
            explanations.append(f"Your {self.client['risk_tolerance'].lower()} risk profile suggests reducing exposure to higher-risk assets.")
        
        # Performance explanation
        if performance > 0.1 and action == "Hold":
            explanations.append(f"Strong year-to-date performance of {performance*100:.1f}% supports maintaining your position.")
        elif performance < -0.05 and action == "Sell":
            explanations.append(f"Poor performance of {performance*100:.1f}% YTD suggests reconsidering this position.")
        
        # Sector-specific explanation
        if sector_outlook > 0.08 and action in ["Hold", "Increase Allocation"]:
            explanations.append(f"Sector forecasts predict continued growth in the coming months.")
        elif sector_outlook < -0.03 and action in ["Reduce Allocation", "Sell"]:
            explanations.append(f"Sector analysis indicates potential headwinds in the near future.")
        
        # Goal alignment explanation
        if self.factors["goal_alignment_factor"] > 1.1:
            explanations.append(f"This position aligns well with your {self.client['financial_goal'].lower()} goal.")
        elif self.factors["goal_alignment_factor"] < 0.9:
            explanations.append(f"This position may not optimally support your {self.client['financial_goal'].lower()} goal.")
        
        # Select 2-3 relevant explanations
        if len(explanations) > 3:
            explanations = random.sample(explanations, 3)
        
        return " ".join(explanations)
    
    def generate_recommendations(self):
        """Generate personalized investment recommendations"""
        recommendations = []
        
        for holding in self.portfolio["holdings"]:
            # Calculate recommendation score
            score = self._calculate_recommendation_score(holding)
            
            # Get sector outlook
            sector_outlook = self._get_sector_outlook(holding["asset_class"])
            
            # Determine recommendation action
            action = self._get_recommendation_action(score, holding["current_allocation"])
            
            # Calculate allocation change
            allocation_change = self._get_allocation_change(action, holding["current_allocation"])
            
            # Generate explanation
            explanation = self._generate_explanation(holding, action, score, sector_outlook)
            
            # Create recommendation object
            recommendation = {
                "asset_class": holding["asset_class"],
                "current_value": holding["value"],
                "current_allocation": holding["current_allocation"],
                "action": action,
                "allocation_change": allocation_change,
                "target_allocation": holding["current_allocation"] + allocation_change,
                "explanation": explanation,
                "confidence_score": min(abs(score) * 20, 99)
            }
            
            recommendations.append(recommendation)
        
        # Sort by confidence score
        recommendations.sort(key=lambda x: x["confidence_score"], reverse=True)
        
        # Generate overall portfolio advice
        overall_advice = self._generate_overall_advice(recommendations)
        
        return {
            "client_id": self.client["client_id"],
            "client_name": self.client["name"],
            "total_portfolio_value": self.portfolio["total_value"],
            "risk_profile": self.client["risk_tolerance"],
            "investment_factors": self.factors,
            "recommendations": recommendations,
            "overall_advice": overall_advice,
            "generated_at": datetime.now().isoformat(),
            "model_used": "SAP Generative AI Hub (simulated)"
        }
    
    def _generate_overall_advice(self, recommendations):
        """Generate overall portfolio advice"""
        # Analyze recommended actions
        actions = [r["action"] for r in recommendations]
        increase_count = actions.count("Increase Allocation")
        decrease_count = actions.count("Reduce Allocation") + actions.count("Sell")
        
        # Market trend
        market_factor = self.factors["market_trend_factor"]
        risk_factor = self.factors["risk_tolerance_factor"]
        
        # Generate advice
        advice = []
        
        # Market trend advice
        if market_factor > 1.1:
            advice.append("Overall market trends are positive, supporting a slightly more aggressive position in select areas.")
        elif market_factor < 0.9:
            advice.append("Market indicators suggest caution, favoring defensive positions and increased diversification.")
        else:
            advice.append("Current market conditions suggest maintaining your strategic asset allocation with targeted adjustments.")
        
        # Portfolio composition advice
        if increase_count > decrease_count and risk_factor > 1:
            advice.append("Consider increasing exposure to growth-oriented assets while maintaining appropriate diversification.")
        elif decrease_count > increase_count:
            advice.append("Reducing exposure in underperforming sectors may help protect against potential market volatility.")
        else:
            advice.append("Your portfolio appears generally well-aligned with your risk profile and financial goals.")
        
        # Time horizon advice
        time_horizon = self.client["time_horizon"]
        if time_horizon > 15:
            advice.append(f"With your {time_horizon}-year time horizon, focusing on long-term growth remains appropriate despite short-term market fluctuations.")
        elif 5 <= time_horizon <= 15:
            advice.append(f"Your {time_horizon}-year time horizon supports a balanced approach with both growth and capital preservation elements.")
        else:
            advice.append(f"Given your shorter {time_horizon}-year time horizon, capital preservation should be emphasized alongside selective growth opportunities.")
        
        return advice

