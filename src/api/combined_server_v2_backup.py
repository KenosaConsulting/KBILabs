#!/usr/bin/env python3
from flask import Flask, send_from_directory, request, jsonify, Response
from flask_cors import CORS
import requests
import os
import json

app = Flask(__name__, static_folder='kbi_dashboard')
CORS(app)

# Cache for companies data
companies_cache = None

@app.route('/')
def index():
    return send_from_directory('kbi_dashboard', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('kbi_dashboard', path)

@app.route('/api/companies', methods=['GET'])
def get_companies():
    global companies_cache
    
    # Try to get from API first
    try:
        response = requests.get("http://localhost:5000/api/companies", timeout=5)
        if response.status_code == 200:
            companies_cache = response.json()
            return jsonify(companies_cache)
    except:
        pass
    
    # If API fails, use cache or load from database
    if companies_cache:
        return jsonify(companies_cache)
    
    # Load directly from database as fallback
    try:
        import psycopg2
        from db_config import get_db_connection
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT uei, organization_name, city, state, 
                   pe_investment_score, business_health_grade,
                   federal_contracts_count, federal_contracts_value,
                   primary_naics, patent_count, nsf_total_funding,
                   phone_number, email, website, sam_registration_status
            FROM enriched_companies 
            ORDER BY pe_investment_score DESC 
            LIMIT 100
        """)
        
        companies = []
        for row in cur.fetchall():
            companies.append({
                'uei': row[0],
                'organization_name': row[1],
                'city': row[2],
                'state': row[3],
                'pe_investment_score': row[4],
                'business_health_grade': row[5],
                'federal_contracts_count': row[6],
                'federal_contracts_value': row[7],
                'primary_naics': row[8],
                'patent_count': row[9],
                'nsf_total_funding': row[10],
                'phone_number': row[11],
                'email': row[12],
                'website': row[13],
                'sam_registration_status': row[14]
            })
        
        conn.close()
        companies_cache = companies
        return jsonify(companies)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/companies/<uei>', methods=['GET'])
def get_company(uei):
    # Get all companies and find the one with matching UEI
    companies = get_companies().json
    
    if isinstance(companies, list):
        for company in companies:
            if company.get('uei') == uei:
                return jsonify(company)
    
    return jsonify({"error": "Company not found"}), 404

@app.route('/api/insights/<uei>', methods=['GET'])
def proxy_insights(uei):
    params = request.args.to_dict()
    try:
        response = requests.get(f"http://localhost:5001/api/insights/{uei}", params=params, timeout=30)
        return response.json()
    except requests.exceptions.Timeout:
        return jsonify({"error": "AI insights timeout - try again"}), 504
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "service": "Combined Server"})

if __name__ == '__main__':
    print("Starting Combined Server v2 on port 8090...")
    
    # Install required packages
    os.system('pip install requests flask flask-cors psycopg2-binary')
    
    # Create necessary directories
    os.makedirs('kbi_dashboard', exist_ok=True)
    
    app.run(host='0.0.0.0', port=8090, debug=False)
