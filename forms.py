from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, TextAreaField, SelectField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional
from models import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class CompanyRegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Confirm Password', 
                              validators=[DataRequired(), EqualTo('password')])
    company_name = StringField('Company Name', validators=[DataRequired(), Length(max=200)])
    contact_person = StringField('Contact Person', validators=[DataRequired(), Length(max=100)])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(max=20)])
    website = StringField('Website', validators=[Optional(), Length(max=200)])
    company_description = TextAreaField('Company Description', validators=[Optional()])
    submit = SubmitField('Register Company')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please use a different email.')

class JobForm(FlaskForm):
    title = StringField('Job Title (English)', validators=[DataRequired(), Length(max=200)])
    title_ar = StringField('Job Title (Arabic)', validators=[Optional(), Length(max=200)])
    department = StringField('Department (English)', validators=[DataRequired(), Length(max=100)])
    department_ar = StringField('Department (Arabic)', validators=[Optional(), Length(max=100)])
    description = TextAreaField('Job Description (English)', validators=[DataRequired()])
    description_ar = TextAreaField('Job Description (Arabic)', validators=[Optional()])
    requirements = TextAreaField('Requirements (English)', validators=[Optional()])
    requirements_ar = TextAreaField('Requirements (Arabic)', validators=[Optional()])
    location = StringField('Location (English)', validators=[DataRequired(), Length(max=100)])
    location_ar = StringField('Location (Arabic)', validators=[Optional(), Length(max=100)])
    employment_type = SelectField('Employment Type', 
                                  choices=[('full-time', 'Full Time'), 
                                          ('part-time', 'Part Time'), 
                                          ('contract', 'Contract')],
                                  validators=[DataRequired()])
    salary_range = StringField('Salary Range (Optional)', validators=[Optional(), Length(max=100)])
    submit = SubmitField('Post Job')

class ApplicationForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(max=20)])
    cover_letter = TextAreaField('Cover Letter', validators=[Optional()])
    cv_file = FileField('Upload CV', 
                        validators=[FileRequired(), 
                                   FileAllowed(['pdf', 'doc', 'docx'], 
                                             'Only PDF and Word documents are allowed!')])
    submit = SubmitField('Submit Application')

class ApplicationUpdateForm(FlaskForm):
    status = SelectField('Status', 
                        choices=[('new', 'New'), 
                                ('contacted', 'Contacted'), 
                                ('rejected', 'Rejected'), 
                                ('hired', 'Hired')],
                        validators=[DataRequired()])
    notes = TextAreaField('Internal Notes', validators=[Optional()])
    submit = SubmitField('Update Application')

class JobSearchForm(FlaskForm):
    search_query = StringField('Search Jobs', validators=[Optional()])
    department = SelectField('Department', choices=[], validators=[Optional()])
    location = SelectField('Location', choices=[], validators=[Optional()])
    employment_type = SelectField('Employment Type', 
                                  choices=[('', 'All Types'),
                                          ('full-time', 'Full Time'), 
                                          ('part-time', 'Part Time'), 
                                          ('contract', 'Contract')],
                                  validators=[Optional()])
    submit = SubmitField('Search')
