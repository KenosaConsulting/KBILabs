#!/usr/bin/env python3
"""Generate a summary report of the enriched data"""

import sys
sys.path.insert(0, '.')

from src.database.connection import SessionLocal
from src.enrichment.models import EnrichedCompany
import pandas as pd

db = SessionLocal()

# Get summary statistics
total = db.query(EnrichedCompany).count()
avg_score = db.query(EnrichedCompany).with_entities(
    EnrichedCompany.pe_investment_score
).all()
scores = [s[0] for s in avg_score if s[0] is not None]

# Grade distribution
grades = db.query(EnrichedCompany.business_health_grade).all()
grade_dist = pd.Series([g[0] for g in grades]).value_counts()

# Top industries
top_industries = db.query(
    EnrichedCompany.primary_naics,
    EnrichedCompany.pe_investment_score
).filter(EnrichedCompany.primary_naics.isnot(None)).all()

# Top locations
top_states = db.query(
    EnrichedCompany.state,
    EnrichedCompany.pe_investment_score
).filter(EnrichedCompany.state.isnot(None)).all()

print("\n=== KBI LABS ENRICHMENT REPORT ===")
print(f"\nTotal Companies Analyzed: {total:,}")
print(f"\nPE Investment Score Statistics:")
print(f"  Average: {sum(scores)/len(scores):.1f}")
print(f"  Highest: {max(scores):.1f}")
print(f"  Lowest: {min(scores):.1f}")

print(f"\nBusiness Health Distribution:")
for grade in ['A', 'B', 'C', 'D', 'F']:
    count = grade_dist.get(grade, 0)
    pct = (count / total * 100) if total > 0 else 0
    print(f"  Grade {grade}: {count} ({pct:.1f}%)")

print(f"\nTop Investment Opportunities:")
top_companies = db.query(EnrichedCompany).order_by(
    EnrichedCompany.pe_investment_score.desc()
).limit(10).all()

for i, company in enumerate(top_companies, 1):
    print(f"\n  {i}. {company.organization_name}")
    print(f"     Score: {company.pe_investment_score:.1f} | Grade: {company.business_health_grade}")
    print(f"     Location: {company.city}, {company.state}")
    print(f"     Industry: NAICS {company.primary_naics}")

db.close()
