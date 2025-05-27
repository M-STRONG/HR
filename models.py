from app import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)  # 'company', 'admin'
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Company-specific fields
    company_name = db.Column(db.String(200))
    company_description = db.Column(db.Text)
    contact_person = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    website = db.Column(db.String(200))
    
    # Relationships
    jobs = db.relationship('Job', backref='company', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        # للاختبار: مقارنة مباشرة بدون تشفير
        if self.password_hash == password:
            return True
        # إذا كانت كلمة المرور مشفرة، استخدم الطريقة العادية
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.email}>'

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    title_ar = db.Column(db.String(200))
    department = db.Column(db.String(100), nullable=False)
    department_ar = db.Column(db.String(100))
    description = db.Column(db.Text, nullable=False)
    description_ar = db.Column(db.Text)
    requirements = db.Column(db.Text)
    requirements_ar = db.Column(db.Text)
    location = db.Column(db.String(100), nullable=False)
    location_ar = db.Column(db.String(100))
    employment_type = db.Column(db.String(50), nullable=False)  # full-time, part-time, contract
    salary_range = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign key
    company_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Relationships
    applications = db.relationship('Application', backref='job', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Job {self.title}>'

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    cover_letter = db.Column(db.Text)
    cv_filename = db.Column(db.String(255))
    status = db.Column(db.String(20), default='new')  # new, contacted, rejected, hired
    notes = db.Column(db.Text)  # Internal notes from HR
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign key
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    
    def __repr__(self):
        return f'<Application {self.full_name} for {self.job.title}>'
