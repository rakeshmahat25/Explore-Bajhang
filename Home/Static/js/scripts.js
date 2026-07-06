// Explore Bajhang - Modern JavaScript
// Performance-focused, accessible, modular

document.addEventListener('DOMContentLoaded', function() {
    initLazyLoading();
    initSmoothScroll();
    initNavbarScroll();
    initSearchEnhancements();
    initImageGallery();
    initChatbot();
    initFormValidation();
    initCountdownTimers();
});

// Lazy loading for images
function initLazyLoading() {
    if ('IntersectionObserver' in window) {
        const lazyImages = document.querySelectorAll('img[loading="lazy"]');
        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    if (img.dataset.src) {
                        img.src = img.dataset.src;
                        img.removeAttribute('data-src');
                    }
                    imageObserver.unobserve(img);
                }
            });
        });
        lazyImages.forEach(img => imageObserver.observe(img));
    }
}

// Smooth scroll for anchor links
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            if (targetId === '#' || targetId === '#!') return;

            const target = document.querySelector(targetId);
            if (target) {
                e.preventDefault();
                const navHeight = document.querySelector('.navbar')?.offsetHeight || 0;
                const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - navHeight - 20;

                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// Navbar scroll effects
function initNavbarScroll() {
    const navbar = document.querySelector('.navbar');
    if (!navbar) return;

    let lastScroll = 0;
    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;

        if (currentScroll > 100) {
            navbar.classList.add('navbar-scrolled');
            navbar.style.background = 'rgba(26, 26, 26, 0.95)';
            navbar.style.backdropFilter = 'blur(10px)';
        } else {
            navbar.classList.remove('navbar-scrolled');
            navbar.style.background = '';
            navbar.style.backdropFilter = '';
        }

        lastScroll = currentScroll;
    }, { passive: true });
}

// Search enhancements - autocomplete
function initSearchEnhancements() {
    const searchInput = document.querySelector('input[name="q"]');
    if (!searchInput || !searchInput.closest('form')) return;

    // Highlight search results if on search page
    if (window.location.pathname.includes('/search')) {
        const query = searchInput.value;
        if (query) {
            highlightSearchTerms(query);
        }
    }
}

function highlightSearchTerms(query) {
    const regex = new RegExp(`(${escapeRegex(query)})`, 'gi');
    document.querySelectorAll('.search-content, mark, .highlight').forEach(el => {
        el.innerHTML = el.innerHTML.replace(regex, '<mark>$1</mark>');
    });
}

function escapeRegex(str) {
    return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

// Image Gallery - Lightbox
function initImageGallery() {
    const galleryItems = document.querySelectorAll('.gallery-item');
    galleryItems.forEach(item => {
        item.addEventListener('click', function() {
            const img = this.querySelector('img');
            if (!img) return;
            openLightbox(img.src, img.alt);
        });

        item.addEventListener('keypress', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                this.click();
            }
        });

        item.setAttribute('tabindex', '0');
        item.setAttribute('role', 'button');
    });
}

function openLightbox(src, alt) {
    const lightbox = document.createElement('div');
    lightbox.className = 'lightbox';
    lightbox.innerHTML = `
        <div class="lightbox-content">
            <button class="lightbox-close" aria-label="Close">&times;</button>
            <img src="${src}" alt="${alt}" />
            <div class="lightbox-caption">${alt}</div>
        </div>
    `;
    document.body.appendChild(lightbox);
    document.body.style.overflow = 'hidden';

    setTimeout(() => lightbox.classList.add('active'), 10);

    function close() {
        lightbox.classList.remove('active');
        setTimeout(() => {
            document.body.removeChild(lightbox);
            document.body.style.overflow = '';
        }, 300);
    }

    lightbox.querySelector('.lightbox-close').addEventListener('click', close);
    lightbox.addEventListener('click', (e) => {
        if (e.target === lightbox) close();
    });

    document.addEventListener('keydown', function escHandler(e) {
        if (e.key === 'Escape') {
            close();
            document.removeEventListener('keydown', escHandler);
        }
    });
}

// Chatbot placeholder
function initChatbot() {
    const chatbot = document.getElementById('chatbotscript');
    if (!chatbot) return;

    chatbot.addEventListener('click', function() {
        alert('Chat feature coming soon! Please use our contact form in the meantime.');
    });
}

// Form validation enhancements
function initFormValidation() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let valid = true;

            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    valid = false;
                    field.classList.add('is-invalid');
                } else {
                    field.classList.remove('is-invalid');
                }
            });

            if (!valid) {
                e.preventDefault();
                const firstInvalid = form.querySelector('.is-invalid');
                if (firstInvalid) firstInvalid.focus();
            }
        });
    });
}

// Countdown timers for events
function initCountdownTimers() {
    document.querySelectorAll('[data-countdown]').forEach(timer => {
        const targetDate = new Date(timer.dataset.countdown).getTime();

        const update = () => {
            const now = new Date().getTime();
            const diff = targetDate - now;

            if (diff <= 0) {
                timer.innerHTML = '<span class="text-danger">Event has passed</span>';
                return;
            }

            const days = Math.floor(diff / (1000 * 60 * 60 * 24));
            const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((diff % (1000 * 60)) / 1000);

            timer.innerHTML = `
                <div class="countdown-item">
                    <span class="countdown-number">${days}</span>
                    <span class="countdown-label">Days</span>
                </div>
                <div class="countdown-item">
                    <span class="countdown-number">${hours}</span>
                    <span class="countdown-label">Hours</span>
                </div>
                <div class="countdown-item">
                    <span class="countdown-number">${minutes}</span>
                    <span class="countdown-label">Minutes</span>
                </div>
                <div class="countdown-item">
                    <span class="countdown-number">${seconds}</span>
                    <span class="countdown-label">Seconds</span>
                </div>
            `;
        };

        update();
        setInterval(update, 1000);
    });
}

// Auto-dismiss alerts
setTimeout(() => {
    document.querySelectorAll('.alert').forEach(alert => {
        const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
        if (bsAlert) bsAlert.close();
    });
}, 5000);
