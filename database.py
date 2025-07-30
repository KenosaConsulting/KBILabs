import os
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Dict, Optional
import logging

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'kbi_labs'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'postgres')
}

class Database:
    def __init__(self):
        self.connection = None
        self.connect()
    
    def connect(self):
        try:
            self.connection = psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)
            logging.info("Database connection established")
        except Exception as e:
            logging.error(f"Failed to connect to database: {e}")
            raise
    
    def disconnect(self):
        if self.connection:
            self.connection.close()
    
    def execute_query(self, query: str, params: tuple = None) -> List[Dict]:
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
        except Exception as e:
            logging.error(f"Query execution failed: {e}")
            self.connection.rollback()
            raise
    
    def execute_insert(self, query: str, params: tuple = None) -> int:
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                self.connection.commit()
                return cursor.lastrowid
        except Exception as e:
            logging.error(f"Insert failed: {e}")
            self.connection.rollback()
            raise

# Create a singleton instance
db = Database()
