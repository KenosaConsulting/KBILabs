#!/usr/bin/env python3
import requests
import json
from datetime import datetime

print("🚀 KBI Labs Platform Summary")
print("=" * 50)
print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("\n📊 PLATFORM CAPABILITIES:")
print("- AI-Powered Investment Analysis (GPT-4)")
print("- 64,000+ Enriched Companies")
print("- Federal Contract Tracking")
print("- Innovation Metrics (Patents, R&D)")
print("- Risk/Return Analysis")
print("- Portfolio Optimization Tools")

# Get current stats
try:
    r = requests.get('http://localhost:8090/api/companies')
    companies = r.json()
    
    total_value = sum(c.get('federal_contracts_value', 0) for c in companies)
    avg_score = sum(c.get('pe_investment_score', 0) for c in companies) / len(companies) if companies else 0
    
    print(f"\n📈 CURRENT PORTFOLIO:")
    print(f"- Companies Loaded: {len(companies)}")
    print(f"- Total Contract Value: ${total_value/1000000:.1f}M")
    print(f"- Average PE Score: {avg_score:.1f}")
    print(f"- Top Performers: {sum(1 for c in companies if c.get('pe_investment_score', 0) >= 80)}")
    
    # Industry breakdown
    industries = {}
    for c in companies:
        naics = c.get('primary_naics', '')[:2] if c.get('primary_naics') else 'Unknown'
        industries[naics] = industries.get(naics, 0) + 1
    
    print("\n🏭 INDUSTRY DISTRIBUTION:")
    for naics, count in sorted(industries.items(), key=lambda x: x[1], reverse=True)[:5]:
        industry_map = {
            '54': 'Professional Services',
            '23': 'Construction',
            '33': 'Manufacturing',
            '51': 'Information Technology',
            '62': 'Healthcare'
        }
        industry = industry_map.get(naics, f'NAICS {naics}')
        print(f"- {industry}: {count} companies")
        
except Exception as e:
    print(f"\n⚠️  Could not load stats: {e}")

print("\n🔗 ACCESS POINTS:")
print(f"- Dashboard: http://3.143.232.123:8090")
print(f"- Portfolio Analysis: http://3.143.232.123:8090/portfolio.html")
print(f"- API Health: http://3.143.232.123:8090/api/health")

print("\n✨ KEY FEATURES:")
print("1. Click any company for detailed AI analysis")
print("2. View Analytics tab for charts & visualizations")
print("3. Use Portfolio Analysis for aggregate insights")
print("4. Compare companies side-by-side")
print("5. Export reports and recommendations")

print("\n🎯 INVESTMENT INSIGHTS:")
print("- Strong Buy: PE Score >= 80")
print("- Buy: PE Score >= 70")
print("- Hold: PE Score >= 50")
print("- Sell: PE Score < 50")

print("\n" + "=" * 50)
print("💡 Platform ready for PE investment analysis!")
