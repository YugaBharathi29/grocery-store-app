"""
SAFETY DATABASE INITIALIZATION SCRIPT
Creates missing tables without affecting existing data
"""

import os
from app import app, db, Cart  # Import only the Cart model

def create_missing_tables():
    """Create only missing tables, preserving existing data"""
    
    with app.app_context():
        print("Checking database schema...")
        
        # List of tables that should exist
        required_tables = [
            'user',
            'category', 
            'product',
            'order',
            'order_item',
            'cart'  # This is the new table we need
        ]
        
        # Get current tables in database
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        existing_tables = inspector.get_table_names()
        
        # Find missing tables
        missing_tables = []
        for table in required_tables:
            if table not in existing_tables:
                missing_tables.append(table)
        
        if not missing_tables:
            print("✅ All required tables exist")
            return
        
        print(f"⚠️ Creating missing table(s): {missing_tables}")
        
        # Create only missing tables
        # This uses SQLAlchemy's metadata to create only non-existent tables
        db.metadata.create_all(db.engine, tables=[
            db.metadata.tables[table] for table in missing_tables
        ])
        
        print(f"✅ Created {len(missing_tables)} missing table(s)")
        
        # Verify creation
        remaining_missing = [t for t in required_tables if t not in inspector.get_table_names()]
        if not remaining_missing:
            print("✅ All tables are now present")
        else:
            print(f"❌ Still missing: {remaining_missing}")

def create_admin_user():
    """Create admin user only if it doesn't exist"""
    from werkzeug.security import generate_password_hash
    
    with app.app_context():
        # Check if admin user exists
        from app import User
        admin = User.query.filter_by(username='admin').first()
        
        if not admin:
            print("Creating admin user...")
            admin_user = User(
                username='admin',
                email='admin@grocery.com',
                password_hash=generate_password_hash('admin123'),
                full_name='Admin User',
                phone='1234567890',
                address='Admin Address',
                is_admin=True
            )
            db.session.add(admin_user)
            db.session.commit()
            print("✅ Admin user created")
        else:
            print("✅ Admin user already exists")

if __name__ == '__main__':
    create_missing_tables()
    create_admin_user()
    print("Database initialization completed")
