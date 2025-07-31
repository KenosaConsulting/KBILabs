#!/usr/bin/env python3
"""Production Readiness Verification for KBI Labs Platform"""
import requests
import psycopg2
import redis
from kafka import KafkaProducer, KafkaAdminClient
import json
from datetime import datetime

print("🏁 KBI Labs Production Readiness Check")
print("=" * 50)

results = {
    "timestamp": datetime.utcnow().isoformat(),
    "checks": {}
}

# 1. API Health
print("\n1️⃣ API Gateway Check...")
try:
    # Basic health
    resp = requests.get("http://localhost:8000/health")
    api_health = resp.json()
    
    # Detailed health
    resp = requests.get("http://localhost:8000/health/detailed")
    detailed = resp.json()
    
    # API docs
    resp = requests.get("http://localhost:8000/api/docs")
    docs_available = resp.status_code == 200
    
    results["checks"]["api"] = {
        "status": "✅ PASS",
        "health": api_health["status"],
        "docs": "Available" if docs_available else "Not Available",
        "services": detailed["services"]
    }
    print("   ✅ API Gateway: Operational")
    print(f"   📚 API Docs: http://localhost:8000/api/docs")
except Exception as e:
    results["checks"]["api"] = {"status": "❌ FAIL", "error": str(e)}
    print(f"   ❌ API Gateway: {e}")

# 2. PostgreSQL
print("\n2️⃣ PostgreSQL Database Check...")
try:
    conn = psycopg2.connect(
        host='localhost',
        port=5432,
        database='kbi_labs',
        user='kbi_user',
        password='kbi_secure_pass_2024'
    )
    cursor = conn.cursor()
    
    # Check tables
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name
    """)
    tables = [t[0] for t in cursor.fetchall()]
    
    # Check row counts
    counts = {}
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        counts[table] = cursor.fetchone()[0]
    
    conn.close()
    
    results["checks"]["postgresql"] = {
        "status": "✅ PASS",
        "tables": tables,
        "row_counts": counts
    }
    print(f"   ✅ PostgreSQL: Connected")
    print(f"   📊 Tables: {', '.join(tables)}")
except Exception as e:
    results["checks"]["postgresql"] = {"status": "❌ FAIL", "error": str(e)}
    print(f"   ❌ PostgreSQL: {e}")

# 3. Redis
print("\n3️⃣ Redis Cache Check...")
try:
    r = redis.Redis(host='localhost', port=6379)
    r.ping()
    
    # Test operations
    r.set('test:production', 'ready', ex=60)
    value = r.get('test:production').decode('utf-8')
    
    # Get info
    info = r.info()
    
    results["checks"]["redis"] = {
        "status": "✅ PASS",
        "version": info.get('redis_version'),
        "memory_used": info.get('used_memory_human'),
        "connected_clients": info.get('connected_clients')
    }
    print(f"   ✅ Redis: Connected (v{info.get('redis_version')})")
except Exception as e:
    results["checks"]["redis"] = {"status": "❌ FAIL", "error": str(e)}
    print(f"   ❌ Redis: {e}")

# 4. Kafka
print("\n4️⃣ Kafka Streaming Check...")
try:
    # Check admin
    admin = KafkaAdminClient(
        bootstrap_servers='localhost:9092',
        client_id='production-check'
    )
    
    # Get topics
    topics = admin.list_topics()
    topic_list = [t for t in topics if not t.startswith('_')]
    
    # Test producer
    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    producer.close()
    
    results["checks"]["kafka"] = {
        "status": "✅ PASS",
        "topics": topic_list,
        "broker_count": len(admin._client.cluster.brokers())
    }
    print(f"   ✅ Kafka: Connected")
    print(f"   📋 Topics: {', '.join(topic_list)}")
except Exception as e:
    results["checks"]["kafka"] = {"status": "❌ FAIL", "error": str(e)}
    print(f"   ❌ Kafka: {e}")

# 5. Overall Status
print("\n" + "=" * 50)
all_pass = all(
    check.get("status") == "✅ PASS" 
    for check in results["checks"].values()
)

if all_pass:
    print("🎉 PRODUCTION READY: All systems operational!")
    print("\n📍 Access Points:")
    print("   • API Docs: http://3.143.232.123:8000/api/docs")
    print("   • Kafka UI: http://3.143.232.123:8080")
    print("   • Health: http://3.143.232.123:8000/health")
else:
    print("⚠️  NOT READY: Some systems need attention")

# Save results
with open('production_readiness.json', 'w') as f:
    json.dump(results, f, indent=2)
print(f"\n📄 Full report saved to: production_readiness.json")
