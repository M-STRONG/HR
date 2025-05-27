// Main JavaScript file for HR Recruitment System

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Language switcher functionality
    const languageSwitcher = document.getElementById('languageSwitcher');
    if (languageSwitcher) {
        languageSwitcher.addEventListener('change', function() {
            const selectedLang = this.value;
            window.location.href = `/set_language/${selectedLang}`;
        });
    }

    // Form validation enhancement
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // File upload preview
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(function(input) {
        input.addEventListener('change', function(event) {
            const file = event.target.files[0];
            if (file) {
                const fileInfo = document.createElement('div');
                fileInfo.className = 'mt-2 text-muted small';
                fileInfo.innerHTML = `
                    <i class="fas fa-file-pdf text-danger me-1"></i>
                    ${file.name} (${formatFileSize(file.size)})
                `;
                
                // Remove existing file info
                const existingInfo = input.parentNode.querySelector('.file-info');
                if (existingInfo) {
                    existingInfo.remove();
                }
                
                fileInfo.className += ' file-info';
                input.parentNode.appendChild(fileInfo);
            }
        });
    });

    // Search form auto-submit (debounced)
    const searchInput = document.getElementById('search_query');
    if (searchInput) {
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(function() {
                document.getElementById('searchForm').submit();
            }, 500);
        });
    }

    // Confirmation dialogs for delete actions
    const deleteButtons = document.querySelectorAll('[data-confirm]');
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(event) {
            const message = button.getAttribute('data-confirm');
            if (!confirm(message)) {
                event.preventDefault();
            }
        });
    });

    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Application status update
    const statusForms = document.querySelectorAll('.status-update-form');
    statusForms.forEach(function(form) {
        const statusSelect = form.querySelector('select[name="status"]');
        const notesTextarea = form.querySelector('textarea[name="notes"]');
        
        if (statusSelect) {
            statusSelect.addEventListener('change', function() {
                // Auto-submit form when status changes
                form.submit();
            });
        }
    });

    // Job search filters
    const filterForm = document.getElementById('filterForm');
    if (filterForm) {
        const filterInputs = filterForm.querySelectorAll('select, input');
        filterInputs.forEach(function(input) {
            input.addEventListener('change', function() {
                filterForm.submit();
            });
        });
    }

    // Copy to clipboard functionality
    const copyButtons = document.querySelectorAll('[data-copy]');
    copyButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            const textToCopy = button.getAttribute('data-copy');
            navigator.clipboard.writeText(textToCopy).then(function() {
                // Show temporary success message
                const originalText = button.innerHTML;
                button.innerHTML = '<i class="fas fa-check"></i> Copied!';
                button.classList.add('btn-success');
                button.classList.remove('btn-outline-secondary');
                
                setTimeout(function() {
                    button.innerHTML = originalText;
                    button.classList.remove('btn-success');
                    button.classList.add('btn-outline-secondary');
                }, 2000);
            });
        });
    });

    // Statistics counter animation
    const statNumbers = document.querySelectorAll('.stat-number');
    const animateCounters = function() {
        statNumbers.forEach(function(counter) {
            const target = parseInt(counter.getAttribute('data-count') || counter.textContent);
            const duration = 2000; // 2 seconds
            const increment = target / (duration / 16); // 60fps
            let current = 0;
            
            const updateCounter = function() {
                if (current < target) {
                    current += increment;
                    counter.textContent = Math.ceil(current);
                    requestAnimationFrame(updateCounter);
                } else {
                    counter.textContent = target;
                }
            };
            
            updateCounter();
        });
    };

    // Trigger counter animation when stats are visible
    const statsSection = document.querySelector('.statistics-section');
    if (statsSection) {
        const observer = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    animateCounters();
                    observer.unobserve(entry.target);
                }
            });
        });
        observer.observe(statsSection);
    }

    // RTL support for current language
    const currentLang = document.documentElement.getAttribute('lang');
    if (currentLang === 'ar') {
        document.body.classList.add('rtl');
        document.dir = 'rtl';
    }
});

// Utility functions
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function showLoading(element) {
    if (element) {
        element.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Loading...';
        element.disabled = true;
    }
}

function hideLoading(element, originalText) {
    if (element) {
        element.innerHTML = originalText;
        element.disabled = false;
    }
}

// AJAX helper function
function makeRequest(url, options = {}) {
    const defaultOptions = {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    };
    
    return fetch(url, { ...defaultOptions, ...options })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .catch(error => {
            console.error('Request failed:', error);
            throw error;
        });
}

// Theme management (for future dark mode support)
const ThemeManager = {
    setTheme: function(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
    },
    
    getTheme: function() {
        return localStorage.getItem('theme') || 'light';
    },
    
    init: function() {
        const savedTheme = this.getTheme();
        this.setTheme(savedTheme);
    }
};

// Initialize theme on page load
ThemeManager.init();
