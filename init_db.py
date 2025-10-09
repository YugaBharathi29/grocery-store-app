from app import app, db, User
from werkzeug.security import import generate_password_hash

with app.app_context():
    # Create tables only if they don't exist (preserves existing data)
    print("Creating tables if they don't exist...")
    db.create_all()
    
    # Check if admin user already exists before creating
    existing_admin = User.query.filter_by(username='admin').first()
    
    if not existing_admin:
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
    else:
        print("Admin user already exists. Skipping creation.")
