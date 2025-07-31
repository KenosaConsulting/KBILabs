#!/usr/bin/env python3
"""Update API to use working PostgreSQL"""
import psycopg2

# Test connection
try:
    conn = psycopg2.connect(
        host='localhost',
        port=5432,
        database='kbi_labs',
        user='kbi_user',
        password='kbi_secure_pass_2024'
    )
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM companies")
    count = cursor.fetchone()[0]
    print(f"✅ PostgreSQL working! Found {count} companies.")
    conn.close()
except Exception as e:
    print(f"❌ Error: {e}")
