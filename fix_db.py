"""
Database fix script - runs directly on Render
Creates cart table with proper PostgreSQL syntax
"""

import os
import sys
from urllib.parse import urlparse
import psycopg2
from app import app, db

def fix_database():
    """Fix database schema issues"""
    with app.app_context():
        try:
            # Get database URL from environment
            database_url = os.environ.get('DATABASE_URL')
            if not database_url:
                print("❌ DATABASE_URL not found in environment!")
                return False
            
            print("🚀 Starting database fix...")
            print(f"🔗 Database URL: {database_url.replace(os.environ.get('DB_PASSWORD', ''), '***')}")
            
            # Parse the database URL
            url = urlparse(database_url)
            
            # Connect to PostgreSQL directly
            conn = psycopg2.connect(
                host=url.hostname,
                database=url.path[1:],
                user=url.username,
                password=url.password,
                port=url.port
            )
            
            cursor = conn.cursor()
            
            # Create cart table with proper syntax
            create_table_sql = '''
            CREATE TABLE IF NOT EXISTS cart (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL DEFAULT 1,
                created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
                FOREIGN KEY (user_id) REFERENCES "user" (id) ON DELETE CASCADE,
                FOREIGN KEY (product_id) REFERENCES product (id) ON DELETE CASCADE,
                CONSTRAINT unique_user_product UNIQUE (user_id, product_id)
            );
            '''
            
            cursor.execute(create_table_sql)
            conn.commit()
            print("✅ Cart table created successfully!")
            
            # Verify table exists
            cursor.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'cart')")
            exists = cursor.fetchone()[0]
            print(f"🔍 Cart table exists: {exists}")
            
            # List all tables
            cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name")
            tables = cursor.fetchall()
            print("\n📋 Tables in database:")
            for table in tables:
                print(f"  • {table[0]}")
            
            cursor.close()
            conn.close()
            print("🎉 Database fix completed successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error fixing database: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    success = fix_database()
    sys.exit(0 if success else 1)
