# KBI Labs Intelligence Platform

A comprehensive business intelligence platform that democratizes data insights for small businesses and investors.

## 🚀 Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/KenosacConsulting/KBILabs.git
   cd KBILabs
   ```

2. **Run the setup script**
   ```bash
   chmod +x scripts/setup_dev.sh
   ./scripts/setup_dev.sh
   ```

3. **Access the platform**
   - API Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health
   - Neo4j Browser: http://localhost:7474

## 🏗️ Architecture

- **FastAPI** - High-performance Python web framework
- **PostgreSQL** - Structured data storage
- **MongoDB** - Unstructured data and analytics
- **Neo4j** - Graph database for relationships
- **Redis** - Caching and session management
- **Kafka** - Real-time data streaming

## 🎯 Platforms

### Alpha Platform (Investment Intelligence)
- Deal discovery and analysis
- Market intelligence
- Due diligence automation

### Compass Platform (SMB Intelligence)  
- Operational benchmarking
- Best practices recommendations
- Growth planning tools

## 📊 Data Processing

The platform processes 250M+ daily data points from:
- Government databases (USAspending, SAM.gov)
- Social media firehose
- Commercial data sources
- Academic research

## 🔧 Development

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop services
docker-compose down
```

## 📈 Mission

To democratize business intelligence by transforming raw data into actionable insights that empower small businesses to compete and investors to discover hidden opportunities.
