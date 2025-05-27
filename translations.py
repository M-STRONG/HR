from flask import session

# Translation dictionaries
TRANSLATIONS = {
    'en': {
        # Navigation
        'home': 'Home',
        'jobs': 'Jobs',
        'login': 'Login',
        'register': 'Register Company',
        'logout': 'Logout',
        'dashboard': 'Dashboard',
        'language': 'Language',
        
        # Common
        'submit': 'Submit',
        'cancel': 'Cancel',
        'edit': 'Edit',
        'delete': 'Delete',
        'save': 'Save',
        'search': 'Search',
        'filter': 'Filter',
        'clear': 'Clear',
        'back': 'Back',
        'next': 'Next',
        'previous': 'Previous',
        'loading': 'Loading...',
        'no_results': 'No results found',
        
        # Authentication
        'email': 'Email',
        'password': 'Password',
        'confirm_password': 'Confirm Password',
        'remember_me': 'Remember Me',
        'sign_in': 'Sign In',
        'sign_up': 'Sign Up',
        'login_required': 'Please log in to access this page',
        'invalid_credentials': 'Invalid email or password',
        'login_success': 'Successfully logged in',
        'logout_success': 'Successfully logged out',
        'registration_success': 'Company registered successfully! You can now log in.',
        'access_denied': 'Access denied',
        
        # Company Registration
        'company_name': 'Company Name',
        'contact_person': 'Contact Person',
        'phone_number': 'Phone Number',
        'website': 'Website',
        'company_description': 'Company Description',
        'register_company': 'Register Company',
        
        # Jobs
        'job_title': 'Job Title',
        'department': 'Department',
        'location': 'Location',
        'employment_type': 'Employment Type',
        'full_time': 'Full Time',
        'part_time': 'Part Time',
        'contract': 'Contract',
        'salary_range': 'Salary Range',
        'job_description': 'Job Description',
        'requirements': 'Requirements',
        'post_job': 'Post Job',
        'view_jobs': 'View Jobs',
        'active_jobs': 'Active Jobs',
        'inactive_jobs': 'Inactive Jobs',
        'job_posted_success': 'Job posted successfully!',
        'all_departments': 'All Departments',
        'all_locations': 'All Locations',
        'apply_now': 'Apply Now',
        'job_details': 'Job Details',
        'company_info': 'Company Information',
        
        # Applications
        'full_name': 'Full Name',
        'cover_letter': 'Cover Letter',
        'upload_cv': 'Upload CV',
        'submit_application': 'Submit Application',
        'application_success': 'Application submitted successfully!',
        'applications': 'Applications',
        'view_applications': 'View Applications',
        'application_status': 'Status',
        'application_date': 'Application Date',
        'new': 'New',
        'contacted': 'Contacted',
        'rejected': 'Rejected',
        'hired': 'Hired',
        'internal_notes': 'Internal Notes',
        'update_status': 'Update Status',
        'application_updated': 'Application updated successfully',
        'download_cv': 'Download CV',
        
        # Dashboard
        'welcome_back': 'Welcome back',
        'total_jobs': 'Total Jobs',
        'total_applications': 'Total Applications',
        'new_applications': 'New Applications',
        'recent_jobs': 'Recent Jobs',
        'recent_applications': 'Recent Applications',
        'company_dashboard': 'Company Dashboard',
        'admin_dashboard': 'Admin Dashboard',
        'statistics': 'Statistics',
        'recent_activity': 'Recent Activity',
        
        # Admin
        'total_companies': 'Total Companies',
        'active_companies': 'Active Companies',
        'recent_companies': 'Recent Companies',
        'manage_companies': 'Manage Companies',
        'company': 'Company',
        'activated': 'activated',
        'deactivated': 'deactivated',
        'job': 'Job',
        
        # Messages
        'success': 'Success',
        'error': 'Error',
        'warning': 'Warning',
        'info': 'Information',
        
        # Homepage
        'hero_title': 'Find Your Next Opportunity',
        'hero_subtitle': 'Connect with top companies and discover amazing career opportunities',
        'browse_jobs': 'Browse Jobs',
        'for_companies': 'For Companies',
        'post_jobs_easily': 'Post Jobs Easily',
        'manage_applications': 'Manage Applications',
        'find_talent': 'Find the Right Talent',
        
        # Footer
        'powered_by': 'Powered by Talent Recruitment System',
        'all_rights_reserved': 'All rights reserved'
    },
    'ar': {
        # Navigation
        'home': 'الرئيسية',
        'jobs': 'الوظائف',
        'login': 'تسجيل الدخول',
        'register': 'تسجيل شركة',
        'logout': 'تسجيل الخروج',
        'dashboard': 'لوحة التحكم',
        'language': 'اللغة',
        
        # Common
        'submit': 'إرسال',
        'cancel': 'إلغاء',
        'edit': 'تعديل',
        'delete': 'حذف',
        'save': 'حفظ',
        'search': 'بحث',
        'filter': 'تصفية',
        'clear': 'مسح',
        'back': 'رجوع',
        'next': 'التالي',
        'previous': 'السابق',
        'loading': 'جاري التحميل...',
        'no_results': 'لا توجد نتائج',
        
        # Authentication
        'email': 'البريد الإلكتروني',
        'password': 'كلمة المرور',
        'confirm_password': 'تأكيد كلمة المرور',
        'remember_me': 'تذكرني',
        'sign_in': 'تسجيل الدخول',
        'sign_up': 'إنشاء حساب',
        'login_required': 'يرجى تسجيل الدخول للوصول إلى هذه الصفحة',
        'invalid_credentials': 'البريد الإلكتروني أو كلمة المرور غير صحيحة',
        'login_success': 'تم تسجيل الدخول بنجاح',
        'logout_success': 'تم تسجيل الخروج بنجاح',
        'registration_success': 'تم تسجيل الشركة بنجاح! يمكنك الآن تسجيل الدخول.',
        'access_denied': 'الوصول مرفوض',
        
        # Company Registration
        'company_name': 'اسم الشركة',
        'contact_person': 'الشخص المسؤول',
        'phone_number': 'رقم الهاتف',
        'website': 'الموقع الإلكتروني',
        'company_description': 'وصف الشركة',
        'register_company': 'تسجيل الشركة',
        
        # Jobs
        'job_title': 'عنوان الوظيفة',
        'department': 'القسم',
        'location': 'الموقع',
        'employment_type': 'نوع التوظيف',
        'full_time': 'دوام كامل',
        'part_time': 'دوام جزئي',
        'contract': 'عقد',
        'salary_range': 'نطاق الراتب',
        'job_description': 'وصف الوظيفة',
        'requirements': 'المتطلبات',
        'post_job': 'نشر وظيفة',
        'view_jobs': 'عرض الوظائف',
        'active_jobs': 'الوظائف النشطة',
        'inactive_jobs': 'الوظائف غير النشطة',
        'job_posted_success': 'تم نشر الوظيفة بنجاح!',
        'all_departments': 'جميع الأقسام',
        'all_locations': 'جميع المواقع',
        'apply_now': 'قدم الآن',
        'job_details': 'تفاصيل الوظيفة',
        'company_info': 'معلومات الشركة',
        
        # Applications
        'full_name': 'الاسم الكامل',
        'cover_letter': 'خطاب التقديم',
        'upload_cv': 'رفع السيرة الذاتية',
        'submit_application': 'إرسال الطلب',
        'application_success': 'تم إرسال الطلب بنجاح!',
        'applications': 'الطلبات',
        'view_applications': 'عرض الطلبات',
        'application_status': 'حالة الطلب',
        'application_date': 'تاريخ التقديم',
        'new': 'جديد',
        'contacted': 'تم التواصل',
        'rejected': 'مرفوض',
        'hired': 'تم التوظيف',
        'internal_notes': 'ملاحظات داخلية',
        'update_status': 'تحديث الحالة',
        'application_updated': 'تم تحديث الطلب بنجاح',
        'download_cv': 'تحميل السيرة الذاتية',
        
        # Dashboard
        'welcome_back': 'مرحباً بعودتك',
        'total_jobs': 'إجمالي الوظائف',
        'total_applications': 'إجمالي الطلبات',
        'new_applications': 'الطلبات الجديدة',
        'recent_jobs': 'الوظائف الحديثة',
        'recent_applications': 'الطلبات الحديثة',
        'company_dashboard': 'لوحة تحكم الشركة',
        'admin_dashboard': 'لوحة تحكم الإدارة',
        'statistics': 'الإحصائيات',
        'recent_activity': 'النشاط الحديث',
        
        # Admin
        'total_companies': 'إجمالي الشركات',
        'active_companies': 'الشركات النشطة',
        'recent_companies': 'الشركات الحديثة',
        'manage_companies': 'إدارة الشركات',
        'company': 'الشركة',
        'activated': 'مفعلة',
        'deactivated': 'معطلة',
        'job': 'الوظيفة',
        
        # Messages
        'success': 'نجح',
        'error': 'خطأ',
        'warning': 'تحذير',
        'info': 'معلومة',
        
        # Homepage
        'hero_title': 'اعثر على فرصتك القادمة',
        'hero_subtitle': 'تواصل مع أفضل الشركات واكتشف فرص مهنية رائعة',
        'browse_jobs': 'تصفح الوظائف',
        'for_companies': 'للشركات',
        'post_jobs_easily': 'انشر الوظائف بسهولة',
        'manage_applications': 'إدارة الطلبات',
        'find_talent': 'اعثر على المواهب المناسبة',
        
        # Footer
        'powered_by': 'مدعوم من نظام التوظيف الذكي',
        'all_rights_reserved': 'جميع الحقوق محفوظة'
    }
}

def get_current_language():
    """Get current language from session, default to English"""
    return session.get('language', 'en')

def set_language(language):
    """Set language in session"""
    if language in TRANSLATIONS:
        session['language'] = language

def get_text(key, language=None):
    """Get translated text for given key"""
    if language is None:
        language = get_current_language()
    
    return TRANSLATIONS.get(language, {}).get(key, TRANSLATIONS['en'].get(key, key))
