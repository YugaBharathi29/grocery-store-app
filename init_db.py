from app import app, db, User
from werkzeug.security import generate_password_hash

with app.app_context():
    # Drop all tables and recreate (WARNING: deletes all data!)
    print("Dropping all tables...")
    db.drop_all()
    
    print("Creating all tables with new schema...")
    db.create_all()
    
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
    print("Done! Database recreated successfully.")
