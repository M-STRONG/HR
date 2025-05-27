
from app import app, db
from models import User

def create_admin():
    with app.app_context():
        # Check if admin already exists
        admin = User.query.filter_by(email='admin@talent.com').first()
        if admin:
            print("Admin user already exists!")
            return
        
        # Create admin user
        admin = User(
            email='admin@talent.com',
            user_type='admin',
            is_active=True
        )
        admin.set_password('admin123')  # Default password
        
        db.session.add(admin)
        db.session.commit()
        
        print("Admin user created successfully!")
        print("Email: admin@talent.com")
        print("Password: admin123")
        print("Please change the password after first login.")

if __name__ == '__main__':
    create_admin()
