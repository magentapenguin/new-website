const picker = document.getElementById('theme-picker');
var theme = localStorage.getItem('theme') ?? 'auto';
// If the user has already set a theme, apply it
const setTheme = (theme) => {
    localStorage.setItem('theme', theme);
    theme = theme;
    picker.querySelectorAll('[data-value]').forEach(option => {
        if (option.dataset.value === theme) {
            option.classList.add('active');
        } else {
            option.classList.remove('active');
        }
    });
    if (theme === 'auto') {
        applyTheme(window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    } else {
        applyTheme(theme);
    }
}
const applyTheme = (theme) => {
    document.documentElement.setAttribute('data-bs-theme', theme);
}

setTheme(theme);

// Watch for changes to localStorage
window.addEventListener('storage', e => {
    if (e.key === 'theme') {
        setTheme(e.newValue);
    }
});

// If the user has set the theme to auto, listen for changes in the system theme
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
    if (theme === 'auto') {
        applyTheme(e.matches ? 'dark' : 'light');
    }
});

picker.querySelectorAll('[data-value]').forEach(option => {
    option.addEventListener('click', e => {
        setTheme(option.dataset.value);
    });
});