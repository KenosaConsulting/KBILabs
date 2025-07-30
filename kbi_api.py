from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import uvicorn
import logging
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

app = FastAPI(title="KBI Labs API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection function
def get_db_connection():
    return psycopg2.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        port=os.getenv('DB_PORT', '5432'),
        database=os.getenv('DB_NAME', 'kbi_enriched'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', 'postgres'),
        cursor_factory=RealDictCursor
    )

@app.get("/")
def read_root():
    return {"message": "KBI Labs API is running"}

@app.get("/api/v1/companies")
def get_companies(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    search: Optional[str] = None
):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Build the query for enriched_companies table
        query = """
            SELECT 
                id,
                company_name as name,
                industry,
                headquarters_location as location,
                website,
                number_of_employees as employees,
                annual_revenue as revenue,
                kbi_score,
                enrichment_status,
                last_updated as last_enriched,
                patents_count as patent_count,
                grants_count as grant_count
            FROM enriched_companies
            WHERE 1=1
        """
        
        params = []
        
        # Add search filter
        if search:
            query += " AND (LOWER(company_name) LIKE LOWER(%s) OR LOWER(industry) LIKE LOWER(%s))"
            search_pattern = f"%{search}%"
            params.extend([search_pattern, search_pattern])
        
        # Add ordering and pagination
        query += """
            ORDER BY kbi_score DESC NULLS LAST
            LIMIT %s OFFSET %s
        """
        params.extend([limit, skip])
        
        # Execute query
        cursor.execute(query, params)
        companies = cursor.fetchall()
        
        # Get total count
        count_query = """
            SELECT COUNT(*) as total
            FROM enriched_companies
            WHERE 1=1
        """
        count_params = []
        
        if search:
            count_query += " AND (LOWER(company_name) LIKE LOWER(%s) OR LOWER(industry) LIKE LOWER(%s))"
            count_params.extend([search_pattern, search_pattern])
        
        cursor.execute(count_query, count_params)
        total_result = cursor.fetchone()
        total_count = total_result['total'] if total_result else 0
        
        # Format the response
        formatted_companies = []
        for company in companies:
            formatted_companies.append({
                "id": company['id'],
                "name": company['name'] or "Unknown Company",
                "industry": company['industry'] or "Unknown",
                "location": company['location'] or "Unknown",
                "website": company['website'],
                "employees": company['employees'] or 0,
                "revenue": f"{float(company['revenue'])/1000000:.1f}M" if company['revenue'] else "N/A",
                "revenue_raw": company['revenue'],
                "kbi_score": round(company['kbi_score']) if company['kbi_score'] else 0,
                "enrichment_status": company['enrichment_status'] or "pending",
                "last_enriched": str(company['last_enriched']) if company['last_enriched'] else None,
                "patent_count": company['patent_count'] or 0,
                "grant_count": company['grant_count'] or 0
            })
        
        cursor.close()
        conn.close()
        
        return {
            "companies": formatted_companies,
            "totalCount": total_count,
            "skip": skip,
            "limit": limit
        }
        
    except Exception as e:
        logging.error(f"Error fetching companies: {e}")
        # Return sample data if database fails
        return {
            "companies": [
                {
                    "id": 1,
                    "name": "Sample Company (DB Error)",
                    "industry": "Technology",
                    "revenue": "0M",
                    "employees": 0,
                    "kbi_score": 0,
                    "location": "Unknown",
                    "enrichment_status": "error",
                    "patent_count": 0,
                    "grant_count": 0
                }
            ],
            "totalCount": 1,
            "skip": skip,
            "limit": limit,
            "error": str(e)
        }

@app.get("/api/v1/companies/{company_id}")
def get_company(company_id: int):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT 
                id,
                company_name as name,
                industry,
                headquarters_location as location,
                website,
                number_of_employees as employees,
                annual_revenue as revenue,
                kbi_score,
                enrichment_status,
                last_updated as last_enriched,
                patents_count as patent_count,
                grants_count as grant_count,
                certifications_count as certification_count
            FROM enriched_companies
            WHERE id = %s
        """
        
        cursor.execute(query, (company_id,))
        company = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")
        
        return {
            "id": company['id'],
            "name": company['name'],
            "industry": company['industry'],
            "location": company['location'],
            "website": company['website'],
            "employees": company['employees'],
            "revenue": f"{float(company['revenue'])/1000000:.1f}M" if company['revenue'] else "N/A",
            "kbi_score": round(company['kbi_score']) if company['kbi_score'] else 0,
            "enrichment_status": company['enrichment_status'],
            "patent_count": company['patent_count'] or 0,
            "grant_count": company['grant_count'] or 0,
            "certification_count": company['certification_count'] or 0
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error fetching company {company_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/analytics")
def get_analytics():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get summary statistics
        stats_query = """
            SELECT 
                COUNT(*) as total_companies,
                AVG(kbi_score) as avg_kbi_score,
                SUM(annual_revenue) as total_revenue,
                SUM(number_of_employees) as total_employees,
                COUNT(DISTINCT industry) as industry_count
            FROM enriched_companies
            WHERE kbi_score IS NOT NULL
        """
        
        cursor.execute(stats_query)
        stats = cursor.fetchone()
        
        # Get top industries
        industry_query = """
            SELECT 
                industry,
                COUNT(*) as company_count,
                AVG(kbi_score) as avg_score
            FROM enriched_companies
            WHERE industry IS NOT NULL
            GROUP BY industry
            ORDER BY company_count DESC
            LIMIT 5
        """
        
        cursor.execute(industry_query)
        top_industries = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return {
            "totalCompanies": stats['total_companies'] or 0,
            "avgKbiScore": round(stats['avg_kbi_score']) if stats['avg_kbi_score'] else 0,
            "totalRevenue": f"{float(stats['total_revenue'])/1000000:.1f}M" if stats['total_revenue'] else "0",
            "totalEmployees": stats['total_employees'] or 0,
            "industryCount": stats['industry_count'] or 0,
            "topIndustries": [
                {
                    "name": ind['industry'],
                    "count": ind['company_count'],
                    "avgScore": round(ind['avg_score']) if ind['avg_score'] else 0
                }
                for ind in top_industries
            ]
        }
        
    except Exception as e:
        logging.error(f"Error fetching analytics: {e}")
        return {
            "totalCompanies": 0,
            "avgKbiScore": 0,
            "totalRevenue": "0",
            "totalEmployees": 0,
            "industryCount": 0,
            "topIndustries": [],
            "error": str(e)
        }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9999)
