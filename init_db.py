#!/usr/bin/env python3
"""
Database initialization script for Docker container
Runs all SQL migrations from supabase/migrations/ directory
"""

import os
import sys
import glob
from pathlib import Path
import psycopg2
from psycopg2 import sql
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_connection():
    """Create database connection"""
    try:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST', 'db'),
            port=int(os.getenv('DB_PORT', '5432')),
            user=os.getenv('DB_USER', 'proiect_user'),
            password=os.getenv('DB_PASSWORD', 'proiect_password'),
            database=os.getenv('DB_NAME', 'proiect_db')
        )
        logger.info("✓ Database connection successful")
        return conn
    except Exception as e:
        logger.error(f"✗ Database connection failed: {e}")
        raise

def run_migrations(conn):
    """Execute all migration files in order"""
    migrations_dir = Path('supabase/migrations')
    
    if not migrations_dir.exists():
        logger.warning(f"Migrations directory not found: {migrations_dir}")
        return
    
    # Get all .sql files sorted by name (to ensure order)
    migration_files = sorted(glob.glob(str(migrations_dir / '*.sql')))
    
    if not migration_files:
        logger.warning("No migration files found")
        return
    
    cursor = conn.cursor()
    
    for migration_file in migration_files:
        try:
            filename = os.path.basename(migration_file)
            logger.info(f"Running migration: {filename}")
            
            with open(migration_file, 'r', encoding='utf-8') as f:
                migration_sql = f.read()
            
            if migration_sql.strip():  # Only execute if not empty
                cursor.execute(migration_sql)
                logger.info(f"✓ Migration completed: {filename}")
        except Exception as e:
            logger.error(f"✗ Migration failed: {filename} - {e}")
            conn.rollback()
            cursor.close()
            raise
    
    conn.commit()
    cursor.close()
    logger.info("✓ All migrations completed successfully")

def main():
    """Main initialization function"""
    try:
        logger.info("Starting database initialization...")
        conn = get_connection()
        run_migrations(conn)
        conn.close()
        logger.info("✓ Database initialization completed")
        return 0
    except Exception as e:
        logger.error(f"✗ Initialization failed: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
