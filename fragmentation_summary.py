import psycopg2
import json

# Connect to database
conn = psycopg2.connect(
    "postgresql://kbi_user:your_postgres_password_here@localhost:5432/kbi_labs"
)
cur = conn.cursor()

# Get top opportunities
cur.execute("""
    SELECT 
        state,
        naics_code,
        roll_up_opportunity_score,
        total_establishments,
        total_employment,
        small_business_ratio,
        fragmentation_level,
        market_size_annual_payroll
    FROM market_fragmentation_analysis
    ORDER BY roll_up_opportunity_score DESC
""")

print("\n🎯 PE ROLL-UP OPPORTUNITY REPORT")
print("=" * 80)

industry_names = {
    '238': 'Specialty Trade Contractors',
    '423': 'Merchant Wholesalers',
    '541': 'Professional Services'
}

for row in cur.fetchall():
    state, naics, score, establishments, employment, small_biz_ratio, frag_level, payroll = row
    industry = industry_names.get(naics, f"NAICS {naics}")
    
    print(f"\n{industry} in {state}")
    print(f"  Roll-up Score: {score}/100 {'🔥' if score > 57 else '✅' if score > 55 else '📊'}")
    print(f"  Total Targets: {establishments:,}")
    print(f"  Market Size: ${payroll/1_000_000:,.0f}M annual payroll")
    print(f"  Small Business Ratio: {small_biz_ratio:.1%}")
    print(f"  Fragmentation: {frag_level}")
    
    if score > 57:
        print(f"  💡 RECOMMENDATION: Prime roll-up opportunity - initiate platform acquisition")
    elif score > 55:
        print(f"  💡 RECOMMENDATION: Good consolidation play - regional strategy recommended")

# Get companies in fragmented markets
cur.execute("""
    SELECT COUNT(*) 
    FROM companies c
    JOIN market_fragmentation_analysis m 
    ON c.state = m.state 
    AND SUBSTRING(c.primary_naics_code::text, 1, 3) = m.naics_code
    WHERE m.roll_up_opportunity_score > 55
""")

company_count = cur.fetchone()[0]
print(f"\n📊 SUMMARY: Found {company_count:,} companies in fragmented markets ready for consolidation")

conn.close()
