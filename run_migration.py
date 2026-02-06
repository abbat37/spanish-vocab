#!/usr/bin/env python3
"""
Database Migration Runner
Run this script to apply database migrations manually.
Usage: python3 run_migration.py
"""
import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def run_migration():
    """Run the migration SQL script"""
    database_url = os.getenv('DATABASE_URL')

    if not database_url:
        print("❌ ERROR: DATABASE_URL not found in environment variables")
        print("Please set DATABASE_URL or create a .env file")
        sys.exit(1)

    # Convert postgres:// to postgresql:// for SQLAlchemy 2.0
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)

    print(f"📊 Connecting to database...")
    print(f"   Using: {database_url.split('@')[1] if '@' in database_url else 'local database'}")

    try:
        engine = create_engine(database_url)

        # Read migration SQL file
        migration_file = 'migrate_add_user_auth.sql'
        print(f"📖 Reading migration file: {migration_file}")

        with open(migration_file, 'r') as f:
            sql_content = f.read()

        # Execute migration
        print(f"🚀 Applying migration...")
        with engine.connect() as conn:
            # Split by semicolon and execute each statement
            statements = [s.strip() for s in sql_content.split(';') if s.strip() and not s.strip().startswith('--')]

            for i, statement in enumerate(statements, 1):
                if statement:
                    print(f"   Executing statement {i}/{len(statements)}...")
                    conn.execute(text(statement))
                    conn.commit()

        print("✅ Migration completed successfully!")
        print()
        print("Next steps:")
        print("1. Restart your application")
        print("2. Test user registration and login")

    except Exception as e:
        print(f"❌ Migration failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    print("=" * 60)
    print("Database Migration: Add User Authentication")
    print("=" * 60)
    print()
    run_migration()
