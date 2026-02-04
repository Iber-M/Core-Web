/**
 * Core Competent - Main JavaScript
 * Handles mobile menu, scroll animations, smooth scrolling, and form validation
 */

// ========================================
// MOBILE MENU TOGGLE
// ========================================

document.addEventListener('DOMContentLoaded', function () {
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const navLinks = document.querySelector('.nav-links');
    const body = document.body;

    if (mobileMenuToggle) {
        mobileMenuToggle.addEventListener('click', function () {
            navLinks.classList.toggle('active');
            mobileMenuToggle.classList.toggle('active');

            // Prevent body scroll when menu is open
            if (navLinks.classList.contains('active')) {
                body.style.overflow = 'hidden';
            } else {
                body.style.overflow = '';
            }
        });

        // Close menu when clicking on a link
        const navLinksItems = navLinks.querySelectorAll('a');
        navLinksItems.forEach(link => {
            link.addEventListener('click', function () {
                navLinks.classList.remove('active');
                mobileMenuToggle.classList.remove('active');
                body.style.overflow = '';
            });
        });
    }
});

// ========================================
// AUTO-HIDE NAVBAR ON SCROLL (STABILIZED)
// ========================================

document.addEventListener('DOMContentLoaded', () => {
    let lastScrollY = window.scrollY;
    const header = document.querySelector('header');
    const navLinks = document.querySelector('.nav-links');

    if (!header) return;

    window.addEventListener('scroll', () => {
        const currentScrollY = window.scrollY;

        // Safety: Mobile Menu Open -> ALWAYS Show
        if (navLinks && navLinks.classList.contains('active')) {
            header.classList.remove('navbar-hidden');
            lastScrollY = currentScrollY;
            return;
        }

        // Safari Bounce Fix: Ignore negative scroll
        if (currentScrollY < 0) return;

        // Main Logic:
        // Hide ONLY if:
        // 1. Scrolling Down (current > last)
        // 2. Not at the very top (current > 100)
        // Everything else -> SHOW

        if (currentScrollY > lastScrollY && currentScrollY > 100) {
            header.classList.add('navbar-hidden');
        } else {
            header.classList.remove('navbar-hidden');
        }

        lastScrollY = currentScrollY;
    }, { passive: true });
});


// ========================================
// SCROLL ANIMATIONS
// ========================================

// Intersection Observer for scroll-triggered animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver(function (entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            // Optionally unobserve after animation to improve performance
            // observer.unobserve(entry.target);
        }
    });
}, observerOptions);

// Observe all elements with animation classes
document.addEventListener('DOMContentLoaded', function () {
    const animatedElements = document.querySelectorAll(
        '.animate-fade, .animate-up, .animate-slide'
    );

    animatedElements.forEach(element => {
        observer.observe(element);
    });
});

// ========================================
// SMOOTH SCROLLING
// ========================================

document.addEventListener('DOMContentLoaded', function () {
    // Handle smooth scroll for anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');

    anchorLinks.forEach(link => {
        link.addEventListener('click', function (e) {
            const href = this.getAttribute('href');

            // Skip if it's just "#"
            if (href === '#') {
                e.preventDefault();
                return;
            }

            const targetId = href.substring(1);
            const targetElement = document.getElementById(targetId);

            if (targetElement) {
                e.preventDefault();

                // Calculate offset for fixed header
                const headerHeight = document.querySelector('header')?.offsetHeight || 80;
                const targetPosition = targetElement.offsetTop - headerHeight;

                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
});

// ========================================
// FORM VALIDATION & HANDLING
// ========================================

document.addEventListener('DOMContentLoaded', function () {

    // Contact Form Validation
    const contactForm = document.querySelector('form');

    if (contactForm) {
        contactForm.addEventListener('submit', function (e) {
            e.preventDefault();

            // Get form fields
            const nameField = document.getElementById('name');
            const emailField = document.getElementById('email');
            const messageField = document.getElementById('message');

            // Reset previous errors
            clearErrors();

            let isValid = true;

            // Validate name
            if (nameField && !nameField.value.trim()) {
                showError(nameField, 'Por favor ingrese su nombre');
                isValid = false;
            }

            // Validate email
            if (emailField) {
                const emailValue = emailField.value.trim();
                if (!emailValue) {
                    showError(emailField, 'Por favor ingrese su correo electrónico');
                    isValid = false;
                } else if (!isValidEmail(emailValue)) {
                    showError(emailField, 'Por favor ingrese un correo electrónico válido');
                    isValid = false;
                }
            }

            // Validate message (if exists)
            if (messageField && !messageField.value.trim()) {
                showError(messageField, 'Por favor ingrese un mensaje');
                isValid = false;
            }

            // If form is valid, show success message
            if (isValid) {
                showSuccessMessage(contactForm);
                // Here you would normally send the form data to a backend
                console.log('Form submitted successfully:', {
                    name: nameField?.value,
                    email: emailField?.value,
                    message: messageField?.value
                });

                // Reset form after submission
                setTimeout(() => {
                    contactForm.reset();
                }, 2000);
            }
        });
    }

    // Newsletter Form Validation
    const newsletterForms = document.querySelectorAll('form[action=""], form:not([action])');
    newsletterForms.forEach(form => {
        // Skip if it's the contact form (already handled)
        if (form.querySelector('#name')) return;

        form.addEventListener('submit', function (e) {
            e.preventDefault();

            const emailInput = this.querySelector('input[type="email"]');

            if (emailInput) {
                clearErrors();

                const emailValue = emailInput.value.trim();

                if (!emailValue) {
                    showError(emailInput, 'Por favor ingrese su correo electrónico');
                } else if (!isValidEmail(emailValue)) {
                    showError(emailInput, 'Por favor ingrese un correo electrónico válido');
                } else {
                    showSuccessMessage(form);
                    console.log('Newsletter subscription:', emailValue);

                    setTimeout(() => {
                        form.reset();
                    }, 2000);
                }
            }
        });
    });
});

// ========================================
// HELPER FUNCTIONS
// ========================================

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function showError(field, message) {
    field.style.borderColor = '#ff4444';

    // Create error message element
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    errorDiv.style.color = '#ff4444';
    errorDiv.style.fontSize = '0.85rem';
    errorDiv.style.marginTop = '0.5rem';

    // Insert error message after the field
    field.parentNode.insertBefore(errorDiv, field.nextSibling);
}

function clearErrors() {
    // Remove all error messages
    const errorMessages = document.querySelectorAll('.error-message');
    errorMessages.forEach(msg => msg.remove());

    // Reset border colors
    const inputs = document.querySelectorAll('input, textarea, select');
    inputs.forEach(input => {
        input.style.borderColor = '';
    });

    // Remove success messages
    const successMessages = document.querySelectorAll('.success-message');
    successMessages.forEach(msg => msg.remove());
}

function showSuccessMessage(form) {
    const successDiv = document.createElement('div');
    successDiv.className = 'success-message';
    successDiv.textContent = '¡Gracias! Su mensaje ha sido enviado correctamente.';
    successDiv.style.cssText = `
        background-color: rgba(198, 168, 124, 0.15);
        border-left: 3px solid #C6A87C;
        color: #C6A87C;
        padding: 1rem;
        margin-top: 1rem;
        border-radius: 4px;
        font-size: 0.95rem;
    `;

    form.appendChild(successDiv);
}

// ========================================
// HEADER SCROLL EFFECT (Optional Enhancement)
// ========================================

let lastScroll = 0;
const header = document.querySelector('header');

window.addEventListener('scroll', function () {
    const currentScroll = window.pageYOffset;

    // Add shadow to header when scrolled
    if (currentScroll > 50) {
        header?.classList.add('scrolled');
    } else {
        header?.classList.remove('scrolled');
    }

    lastScroll = currentScroll;
});
