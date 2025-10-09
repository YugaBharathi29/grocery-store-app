"""
Ultimate database initializer
"""

import os
from app import app, db

def create_database():
    with app.app_context():
        print("🚀 Starting database setup...")
        
        try:
            # Create all tables based on models
            db.create_all()
            print("✅ All tables created successfully")
            
            # Verify User table exists
            try:
                from app import User
                print("✅ User model is available")
                
                # Try to query users
                user_count = User.query.count()
                print(f"📊 User table has {user_count} users")
                
            except Exception as e:
                print(f"❌ User model error: {str(e)}")
            
            # Verify Cart table exists
            try:
                from app import Cart
                print("✅ Cart model is available")
                
                # Try to count cart items
                cart_count = Cart.query.count()
                print(f"📊 Cart table has {cart_count} items")
                
            except Exception as e:
                print(f"❌ Cart model error: {str(e)}")
                print("💡 This is OK if it's the first run - the table will be created")
            
            # Create admin user
            create_admin()
            
            # List all tables in database
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"\n📋 Tables in database: {tables}")
            
            if 'cart' in tables:
                print("✅ Cart table is present")
            else:
                print("❌ Cart table is missing - this is a problem")
            
        except Exception as e:
            print(f"❌ Critical error: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
        
        print("🎉 Database setup completed!")
        return True

def create_admin():
    """Create admin user if not exists"""
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

if __name__ == '__main__':
    success = create_database()
    exit(0 if success else 1)
