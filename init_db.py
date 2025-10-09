"""
Database initialization using raw SQL (most reliable method)
"""

import os
from app import app, db

with app.app_context():
    try:
        # Create cart table using raw SQL (most reliable method)
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS cart (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 1,
            created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
            FOREIGN KEY (user_id) REFERENCES user (id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES product (id) ON DELETE CASCADE,
            UNIQUE (user_id, product_id)
        );
        """
        
        db.session.execute(db.text(create_table_sql))
        db.session.commit()
        print("✅ Cart table created successfully!")
        
        # Verify the table exists
        result = db.session.execute(db.text("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'cart'
            );
        """))
        table_exists = result.fetchone()[0]
        
        if table_exists:
            print("✅ Cart table verification: PASSED")
        else:
            print("❌ Cart table verification: FAILED")
        
        # Create admin user if not exists
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
            print("✅ Admin user created")
        else:
            print("✅ Admin user already exists")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        db.session.rollback()
