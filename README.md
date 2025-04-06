# SAP-AI-Investment-Advisor
SAP GenAI-powered Investment Advisor (prototype)

A demonstration of how financial institutions can leverage SAP's AI technologies to generate personalized investment recommendations.

Overview
This project showcases a prototype application that simulates how financial institutions could use SAP's AI infrastructure to analyze client portfolios, market trends, and risk profiles to deliver tailored investment advice. It demonstrates the potential of generative AI in financial advisory services through a practical implementation.

Important Note: This is a demonstration project intended for educational and portfolio purposes only. While SAP provides the underlying AI technologies and infrastructure that could support such applications, SAP does not offer ready-made investment advisory solutions for financial institutions to provide to their end customers. Financial advisory is highly regulated and would require significant customization based on regional regulations and firm-specific investment philosophies.

Installation 

# Clone the repository 
git clone https://github.com/AxelSuffrin/SAP-GenAI-Investment-Advisor.git 
 
# Navigate to the project directory 
cd SAP-GenAI-Investment-Advisor 
 
# Create required directories if they don't exist 
mkdir -p data 
 
# Install dependencies 
pip install -r requirements.txt 
 

The requirements.txt file should contain: 

Flask==2.2.3 
numpy==1.24.2 
Faker==18.3.1 
 

Running the Application 

# Start the Flask development server 
python app.py 
 

After starting the application: 

Open your browser and navigate to http://localhost:5000 

Select a client from the dashboard to view personalized investment recommendations 

Explore how different client profiles generate different asset recommendations 

Notice how the five investment factors (Market Trend, Risk Tolerance, Portfolio Diversification, Age-Based Allocation, and Goal Alignment) influence the recommendations 

The first time you run the application, it will automatically generate mock data including: 

- 100 simulated client profiles with varying risk tolerances and financial goals 
- Portfolio holdings across various asset classes 
- Current market trend simulations 

Key Features
- Personalized Asset Recommendations: AI-generated investment suggestions based on client risk profiles and portfolio analysis
- Multi-factor Decision Engine: Transparent investment factors that explain the reasoning behind recommendations
- Portfolio Analysis: Evaluation of current holdings against financial goals and market conditions
- Dynamic Allocation Adjustments: Specific allocation changes with clear explanations
- Confidence Indicators: Numeric representation of the model's confidence in each recommendation

Technical Implementation
This project demonstrates how various SAP technologies could be integrated:

- SAP Generative AI Hub: Foundation for natural language generation and recommendation explanations
- SAP AI Core: Infrastructure for deployment of predictive models and investment algorithms
- SAP Business Technology Platform: Integration layer connecting to financial data sources
- SAP HANA Cloud: Potential database for efficient portfolio and market analysis

Practical Applications
While this prototype shows investment recommendations for individual clients, the technology could be applied in various financial contexts:

- Advisor Augmentation: Providing financial advisors with AI-generated insights to enhance their recommendations
- Portfolio Analysis: Identifying potential risks or optimization opportunities in existing portfolios
- Client Education: Generating explanations to help clients understand investment rationales
- Operational Efficiency: Automating aspects of portfolio review and rebalancing processes

Development Context
This project was developed as a portfolio demonstration using simulated data. For a real implementation, financial institutions would need to:

- Customize the solution to their specific investment methodologies
- Integrate with their existing financial systems
- Ensure compliance with relevant financial regulations
- Implement appropriate oversight and review mechanisms

Using This Project
This prototype demonstrates concepts only and should not be used for actual investment decisions. It shows how modern AI capabilities could be integrated with financial data to create more personalized and transparent investment experiences.

The UI demonstrates how investment recommendations could be presented with allocation adjustments, confidence levels, and natural language explanations that help users understand the reasoning behind each suggestion.

License
MIT License
This project is not affiliated with or endorsed by SAP SE. All SAP product names are trademarks or registered trademarks of SAP SE or its affiliates.
