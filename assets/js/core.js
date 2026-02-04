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
