// Main JavaScript file for TikTok Downloader

document.addEventListener('DOMContentLoaded', function() {
    // Initialize the application
    initializeApp();
});

function initializeApp() {
    // Initialize URL validation
    initializeUrlValidation();
    
    // Initialize form handling
    initializeFormHandling();
    
    // Initialize download buttons
    initializeDownloadButtons();
    
    // Initialize tooltips and other Bootstrap components
    initializeBootstrapComponents();
}

function initializeUrlValidation() {
    const urlInput = document.querySelector('.url-input');
    if (!urlInput) return;
    
    urlInput.addEventListener('input', function() {
        validateTikTokUrl(this.value);
    });
    
    urlInput.addEventListener('paste', function(e) {
        // Small delay to allow paste to complete
        setTimeout(() => {
            validateTikTokUrl(this.value);
        }, 100);
    });
}

function validateTikTokUrl(url) {
    const urlInput = document.querySelector('.url-input');
    const submitButton = document.querySelector('.download-btn');
    
    if (!url.trim()) {
        resetValidationState();
        return;
    }
    
    const tiktokPatterns = [
        /^https?:\/\/(www\.)?tiktok\.com\/@[^\/]+\/video\/\d+/,
        /^https?:\/\/(www\.)?tiktok\.com\/t\/[A-Za-z0-9]+/,
        /^https?:\/\/vm\.tiktok\.com\/[A-Za-z0-9]+/,
        /^https?:\/\/(www\.)?tiktok\.com\/@[^\/]+\/video\/\d+\?.*/
    ];
    
    const isValid = tiktokPatterns.some(pattern => pattern.test(url));
    
    if (isValid) {
        urlInput.classList.remove('is-invalid');
        urlInput.classList.add('is-valid');
        submitButton.disabled = false;
    } else {
        urlInput.classList.remove('is-valid');
        urlInput.classList.add('is-invalid');
        submitButton.disabled = true;
    }
}

function resetValidationState() {
    const urlInput = document.querySelector('.url-input');
    const submitButton = document.querySelector('.download-btn');
    
    if (urlInput) {
        urlInput.classList.remove('is-valid', 'is-invalid');
    }
    
    if (submitButton) {
        submitButton.disabled = false;
    }
}

function initializeFormHandling() {
    const downloadForm = document.querySelector('.download-form');
    if (!downloadForm) return;
    
    downloadForm.addEventListener('submit', function(e) {
        const urlInput = this.querySelector('.url-input');
        const submitButton = this.querySelector('.download-btn');
        
        if (!urlInput.value.trim()) {
            e.preventDefault();
            showAlert('Please enter a TikTok URL', 'error');
            return;
        }
        
        // Show loading state
        showLoadingState(submitButton);
    });
}

function initializeDownloadButtons() {
    const downloadButtons = document.querySelectorAll('.download-quality-btn');
    
    downloadButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            showLoadingState(this);
            
            // Re-enable button after timeout (in case download doesn't start)
            setTimeout(() => {
                resetButtonState(this);
            }, 10000);
        });
    });
}

function showLoadingState(button) {
    const originalText = button.innerHTML;
    button.setAttribute('data-original-text', originalText);
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
    button.disabled = true;
}

function resetButtonState(button) {
    const originalText = button.getAttribute('data-original-text');
    if (originalText) {
        button.innerHTML = originalText;
        button.disabled = false;
    }
}

function initializeBootstrapComponents() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    const popoverList = popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
}

function showAlert(message, type = 'info') {
    // Create alert element
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    // Insert at top of main content
    const mainContent = document.querySelector('.main-content') || document.body;
    const container = document.createElement('div');
    container.className = 'container';
    container.appendChild(alertDiv);
    
    mainContent.insertBefore(container, mainContent.firstChild);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        if (alertDiv && alertDiv.parentNode) {
            alertDiv.classList.remove('show');
            setTimeout(() => {
                if (alertDiv.parentNode && alertDiv.parentNode.parentNode) {
                    alertDiv.parentNode.parentNode.removeChild(alertDiv.parentNode);
                }
            }, 300);
        }
    }, 5000);
}

// Utility functions
function copyToClipboard(text) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(function() {
            showAlert('Copied to clipboard!', 'success');
        }).catch(function() {
            fallbackCopyToClipboard(text);
        });
    } else {
        fallbackCopyToClipboard(text);
    }
}

function fallbackCopyToClipboard(text) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    textArea.style.left = '-999999px';
    textArea.style.top = '-999999px';
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    
    try {
        document.execCommand('copy');
        showAlert('Copied to clipboard!', 'success');
    } catch (err) {
        showAlert('Failed to copy to clipboard', 'error');
    }
    
    document.body.removeChild(textArea);
}

// Analytics and tracking functions (for future implementation)
function trackEvent(eventName, properties = {}) {
    // Google Analytics or other tracking service integration
    console.log('Event tracked:', eventName, properties);
}

// Performance monitoring
function measurePerformance(name, fn) {
    const start = performance.now();
    const result = fn();
    const end = performance.now();
    console.log(`${name} took ${end - start} milliseconds`);
    return result;
}

// Error handling
window.addEventListener('error', function(e) {
    console.error('JavaScript error:', e.error);
    // Could send to error reporting service
});

// Unhandled promise rejections
window.addEventListener('unhandledrejection', function(e) {
    console.error('Unhandled promise rejection:', e.reason);
    // Could send to error reporting service
});

// Service Worker registration (for future PWA features)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        // navigator.serviceWorker.register('/sw.js')
        //     .then(function(registration) {
        //         console.log('ServiceWorker registration successful');
        //     })
        //     .catch(function(err) {
        //         console.log('ServiceWorker registration failed');
        //     });
    });
}

// Export functions for testing or external use
window.TikTokDownloader = {
    validateTikTokUrl,
    showAlert,
    copyToClipboard,
    trackEvent
};
