// docs/javascripts/extra.js

// Add smooth scrolling to anchor links
document.addEventListener('DOMContentLoaded', function() {
    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Add fade-in animation to feature cards
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '0';
                entry.target.style.transform = 'translateY(20px)';
                
                setTimeout(() => {
                    entry.target.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }, 100);
                
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observe all feature cards
    document.querySelectorAll('.feature-card').forEach(card => {
        observer.observe(card);
    });
    
    // Add copy button tooltip
    const copyButtons = document.querySelectorAll('.md-clipboard');
    copyButtons.forEach(button => {
        button.addEventListener('click', function() {
            const originalTitle = this.getAttribute('title');
            this.setAttribute('title', 'Copied!');
            setTimeout(() => {
                this.setAttribute('title', originalTitle);
            }, 2000);
        });
    });
});

// Console easter egg
console.log('%c🔐 dbcreds', 'font-size: 20px; font-weight: bold; color: #17a2b8;');
console.log('%cSecure credential management for developers', 'color: #28a745;');
console.log('%cLearn more at: https://github.com/Sunnova-ShakesDlamini/dbcreds', 'color: #666;');