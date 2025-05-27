import os
from flask import render_template, request, redirect, url_for, flash, session, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from app import app, db
from models import User, Job, Application
from forms import (LoginForm, CompanyRegistrationForm, JobForm, 
                   ApplicationForm, ApplicationUpdateForm, JobSearchForm)
from utils import login_required, company_required, admin_required, allowed_file
from translations import get_text, get_current_language, set_language

@app.route('/')
def index():
    # Get recent jobs for homepage
    recent_jobs = Job.query.filter_by(is_active=True).order_by(Job.created_at.desc()).limit(6).all()
    return render_template('index.html', recent_jobs=recent_jobs)

@app.route('/set_language/<language>')
def set_language_route(language):
    set_language(language)
    return redirect(request.referrer or url_for('index'))

# Authentication routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data) and user.is_active:
            session['user_id'] = user.id
            session['user_type'] = user.user_type
            flash(get_text('login_success'), 'success')
            
            # Redirect based on user type
            if user.user_type == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('company_dashboard'))
        else:
            flash(get_text('invalid_credentials'), 'error')
    
    return render_template('auth/login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = CompanyRegistrationForm()
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            user_type='company',
            company_name=form.company_name.data,
            contact_person=form.contact_person.data,
            phone=form.phone.data,
            website=form.website.data,
            company_description=form.company_description.data
        )
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        flash(get_text('registration_success'), 'success')
        return redirect(url_for('login'))
    
    return render_template('auth/register.html', form=form)

@app.route('/logout')
def logout():
    session.clear()
    flash(get_text('logout_success'), 'info')
    return redirect(url_for('index'))

# Company routes
@app.route('/company/dashboard')
@login_required
@company_required
def company_dashboard():
    user_id = session['user_id']
    company = User.query.get(user_id)
    jobs = Job.query.filter_by(company_id=user_id).order_by(Job.created_at.desc()).all()
    
    # Get application statistics
    total_applications = 0
    new_applications = 0
    for job in jobs:
        total_applications += len(job.applications)
        new_applications += len([app for app in job.applications if app.status == 'new'])
    
    stats = {
        'total_jobs': len(jobs),
        'active_jobs': len([job for job in jobs if job.is_active]),
        'total_applications': total_applications,
        'new_applications': new_applications
    }
    
    return render_template('company/dashboard.html', company=company, jobs=jobs, stats=stats)

@app.route('/company/post_job', methods=['GET', 'POST'])
@login_required
@company_required
def post_job():
    form = JobForm()
    if form.validate_on_submit():
        job = Job(
            title=form.title.data,
            title_ar=form.title_ar.data,
            department=form.department.data,
            department_ar=form.department_ar.data,
            description=form.description.data,
            description_ar=form.description_ar.data,
            requirements=form.requirements.data,
            requirements_ar=form.requirements_ar.data,
            location=form.location.data,
            location_ar=form.location_ar.data,
            employment_type=form.employment_type.data,
            salary_range=form.salary_range.data,
            company_id=session['user_id']
        )
        
        db.session.add(job)
        db.session.commit()
        
        flash(get_text('job_posted_success'), 'success')
        return redirect(url_for('company_dashboard'))
    
    return render_template('company/post_job.html', form=form)

@app.route('/company/job/<int:job_id>/applications')
@login_required
@company_required
def view_applications(job_id):
    user_id = session['user_id']
    job = Job.query.filter_by(id=job_id, company_id=user_id).first_or_404()
    applications = Application.query.filter_by(job_id=job_id).order_by(Application.applied_at.desc()).all()
    
    return render_template('company/view_applications.html', job=job, applications=applications)

@app.route('/company/application/<int:app_id>/update', methods=['POST'])
@login_required
@company_required
def update_application(app_id):
    application = Application.query.get_or_404(app_id)
    
    # Verify the application belongs to the company
    if application.job.company_id != session['user_id']:
        flash(get_text('access_denied'), 'error')
        return redirect(url_for('company_dashboard'))
    
    status = request.form.get('status')
    notes = request.form.get('notes')
    
    if status in ['new', 'contacted', 'rejected', 'hired']:
        application.status = status
        application.notes = notes
        db.session.commit()
        flash(get_text('application_updated'), 'success')
    
    return redirect(url_for('view_applications', job_id=application.job_id))

@app.route('/company/job/<int:job_id>/toggle_status')
@login_required
@company_required
def toggle_job_status(job_id):
    user_id = session['user_id']
    job = Job.query.filter_by(id=job_id, company_id=user_id).first_or_404()
    
    job.is_active = not job.is_active
    db.session.commit()
    
    status_text = get_text('activated') if job.is_active else get_text('deactivated')
    flash(f"{get_text('job')} {status_text}", 'success')
    
    return redirect(url_for('company_dashboard'))

# Job browsing and application routes
@app.route('/jobs')
def job_list():
    form = JobSearchForm()
    
    # Populate form choices dynamically
    departments = db.session.query(Job.department).filter(Job.is_active == True).distinct().all()
    locations = db.session.query(Job.location).filter(Job.is_active == True).distinct().all()
    
    form.department.choices = [('', get_text('all_departments'))] + [(d[0], d[0]) for d in departments]
    form.location.choices = [('', get_text('all_locations'))] + [(l[0], l[0]) for l in locations]
    
    # Start with active jobs
    query = Job.query.filter_by(is_active=True)
    
    # Apply filters
    if request.args.get('search_query'):
        search_term = f"%{request.args.get('search_query')}%"
        query = query.filter(
            db.or_(
                Job.title.ilike(search_term),
                Job.title_ar.ilike(search_term),
                Job.description.ilike(search_term),
                Job.description_ar.ilike(search_term)
            )
        )
    
    if request.args.get('department'):
        query = query.filter_by(department=request.args.get('department'))
    
    if request.args.get('location'):
        query = query.filter_by(location=request.args.get('location'))
    
    if request.args.get('employment_type'):
        query = query.filter_by(employment_type=request.args.get('employment_type'))
    
    jobs = query.order_by(Job.created_at.desc()).all()
    
    return render_template('jobs/list.html', jobs=jobs, form=form)

@app.route('/jobs/<int:job_id>')
def job_detail(job_id):
    job = Job.query.filter_by(id=job_id, is_active=True).first_or_404()
    return render_template('jobs/detail.html', job=job)

@app.route('/jobs/<int:job_id>/apply', methods=['GET', 'POST'])
def apply_job(job_id):
    job = Job.query.filter_by(id=job_id, is_active=True).first_or_404()
    form = ApplicationForm()
    
    if form.validate_on_submit():
        try:
            # Handle file upload
            cv_file = form.cv_file.data
            filename = None
            if cv_file and cv_file.filename and allowed_file(cv_file.filename):
                filename = secure_filename(cv_file.filename)
                # Add timestamp to avoid conflicts
                import time
                filename = f"{int(time.time())}_{filename}"
                
                # Ensure upload directory exists
                upload_path = os.path.join(app.config['UPLOAD_FOLDER'])
                os.makedirs(upload_path, exist_ok=True)
                
                # Save the file
                file_path = os.path.join(upload_path, filename)
                cv_file.save(file_path)
            
            application = Application(
                full_name=form.full_name.data,
                email=form.email.data,
                phone=form.phone.data,
                cover_letter=form.cover_letter.data,
                cv_filename=filename,
                job_id=job_id
            )
            
            db.session.add(application)
            db.session.commit()
            
            flash(get_text('application_success'), 'success')
            return render_template('application_success.html', job=job)
            
        except Exception as e:
            db.session.rollback()
            flash(get_text('application_error') if get_current_language() == 'en' else 'حدث خطأ أثناء إرسال الطلب. يرجى المحاولة مرة أخرى.', 'error')
            app.logger.error(f"Application submission error: {str(e)}")
    
    return render_template('jobs/apply.html', job=job, form=form)

@app.route('/download_cv/<filename>')
@login_required
def download_cv(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Admin routes
@app.route('/admin/dashboard')
@login_required
@admin_required
def admin_dashboard():
    # Get system statistics
    total_companies = User.query.filter_by(user_type='company').count()
    active_companies = User.query.filter_by(user_type='company', is_active=True).count()
    total_jobs = Job.query.count()
    active_jobs = Job.query.filter_by(is_active=True).count()
    total_applications = Application.query.count()
    
    # Get recent activity
    recent_companies = User.query.filter_by(user_type='company').order_by(User.created_at.desc()).limit(5).all()
    recent_jobs = Job.query.order_by(Job.created_at.desc()).limit(5).all()
    recent_applications = Application.query.order_by(Application.applied_at.desc()).limit(5).all()
    
    stats = {
        'total_companies': total_companies,
        'active_companies': active_companies,
        'total_jobs': total_jobs,
        'active_jobs': active_jobs,
        'total_applications': total_applications
    }
    
    return render_template('admin/dashboard.html', 
                         stats=stats,
                         recent_companies=recent_companies,
                         recent_jobs=recent_jobs,
                         recent_applications=recent_applications)

@app.route('/admin/toggle_company/<int:company_id>')
@login_required
@admin_required
def toggle_company_status(company_id):
    company = User.query.filter_by(id=company_id, user_type='company').first_or_404()
    company.is_active = not company.is_active
    db.session.commit()
    
    status_text = get_text('activated') if company.is_active else get_text('deactivated')
    flash(f"{get_text('company')} {company.company_name} {status_text}", 'success')
    
    return redirect(url_for('admin_dashboard'))

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

# Context processors
@app.context_processor
def inject_globals():
    return {
        'get_text': get_text,
        'get_current_language': get_current_language,
        'current_user': get_current_user()
    }

def get_current_user():
    if 'user_id' in session:
        return User.query.get(session['user_id'])
    return None
