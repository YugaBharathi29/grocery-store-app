from app import app, db, User
from werkzeug.security import generate_password_hash

with app.app_context():
    # Drop all tables and recreate them (WARNING: This deletes all data!)
    db.drop_all()
    db.create_all()
    print("Database tables recreated!")
    
    # Create admin user
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
    print("Admin user created: username=admin, password=admin123")
