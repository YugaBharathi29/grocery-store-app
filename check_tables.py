"""
Check existing database tables
"""

import os
from app import app, db

with app.app_context():
    # List all tables in the database
    result = db.session.execute(db.text("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        ORDER BY table_name;
    """))
    
    tables = result.fetchall()
    print("Tables in database:")
    for table in tables:
        print(f"  • {table[0]}")
    
    # Check if cart table exists
    cart_exists = db.session.execute(db.text("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = 'cart'
        );
    """)).fetchone()[0]
    
    print(f"\nCart table exists: {cart_exists}")
