"""
Fresh database initialization
"""

import os
from app import app, db

with app.app_context():
    print("🎯 Starting fresh database setup...")
    
    # Drop all tables first (won't error if they don't exist)
    try:
        db.drop_all()
        print("🗑️  Dropped all tables")
    except Exception as e:
        print(f"🔧 Table drop attempt: {str(e)} (normal if first time)")
    
    # Create all tables fresh
    db.create_all()
    print("✅ Created all tables")
    
    # Create admin user
    from app import User
    from werkzeug.security import generate_password_hash
    
    admin = User.query.filter_by(username='admin').first()
    if not admin:
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
        print("🔑 Admin user created")
    else:
        print("🔑 Admin user already exists")
    
    print("🎉 Database setup completed!")
