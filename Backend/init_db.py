#!/usr/bin/env python3
"""Database initialization script"""

from database import init_db, engine
from models import Base

def main():
    """Initialize the database"""
    print("Creating database tables...")
    init_db()
    print("Database initialized successfully!")
    
    # Verify tables were created
    print("Created tables:")
    for table_name in Base.metadata.tables.keys():
        print(f"  - {table_name}")

if __name__ == "__main__":
    main()