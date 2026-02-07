/**
 * Core Competent - Theme Switcher Logic
 * Handles toggling between Default (Deep Navy) and Light (Reading Mode) themes.
 * Persists user preference in localStorage.
 */

document.addEventListener('DOMContentLoaded', () => {
    const themeToggleBtn = document.getElementById('theme-toggle');
    const htmlElement = document.documentElement;

    // Theme Configuration: Only Default (Dark) and Light (Reading Mode)
    const themes = ['default', 'light'];

    // Get saved theme or default to 'default'
    let currentTheme = localStorage.getItem('theme') || 'default';

    // Apply initial theme
    function applyTheme(theme) {
        if (theme === 'default') {
            htmlElement.removeAttribute('data-theme');
        } else {
            htmlElement.setAttribute('data-theme', theme);
        }
        updateIcon(theme);
    }

    // Update Icon based on theme
    function updateIcon(theme) {
        if (!themeToggleBtn) return;

        const isLight = theme === 'light';
        // Sun icon for Light Mode, Moon icon for Dark Mode
        themeToggleBtn.innerHTML = isLight
            ? '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>'
            : '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>';

        themeToggleBtn.setAttribute('aria-label', isLight ? 'Cambiar a modo oscuro' : 'Cambiar a modo lectura');
    }

    // Initialize
    if (themeToggleBtn) {
        applyTheme(currentTheme);

        // Toggle Handler
        themeToggleBtn.addEventListener('click', (e) => {
            e.preventDefault();
            const newTheme = currentTheme === 'default' ? 'light' : 'default';
            currentTheme = newTheme;
            applyTheme(newTheme);
            localStorage.setItem('theme', newTheme);
        });
    }
});
