"""
Fix database cart table using direct PostgreSQL connection
"""

import psycopg2
from urllib.parse import urlparse

# Your database connection URL from Render
DATABASE_URL = "postgresql://grocery_store_app_vyur_user:ITjYkVRt9DX5dOfOW8UCKr0ZEUidQ0nf@dpg-d3j58sje5dus739ih8a0-a/grocery_store_app_vyur"

# Parse the URL
url = urlparse(DATABASE_URL)
print("🚇 Connecting to database...")

try:
    # Connect to PostgreSQL
    connection = psycopg2.connect(
        host=url.hostname,
        database=url.path[1:],  # Remove leading '/'
        user=url.username,
        password=url.password,
        port=url.port
    )
    
    cursor = connection.cursor()
    print("✅ Connected to database!")
    
    # Create cart table with proper syntax
    create_table_query = '''
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
    
    cursor.execute(create_table_query)
    connection.commit()
    print("✅ Cart table created/verified")
    
    # Verify the table exists
    cursor.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'cart');")
    table_exists = cursor.fetchone()[0]
    print(f"📋 Cart table exists: {table_exists}")
    
    # Show all tables
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name;")
    tables = cursor.fetchall()
    print("\n📋 Tables in database:")
    for table in tables:
        print(f"  • {table[0]}")
    
    # Close connections
    cursor.close()
    connection.close()
    print("\n🎉 Done! Database fixed.")
    
except Exception as error:
    print(f"❌ Error: {error}")
