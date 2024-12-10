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
    // set the picker to the current theme icon
    picker.querySelector('button').innerHTML = picker.querySelector(`[data-value="${theme}"] > i`).outerHTML+'<span class="visually-hidden">Color Theme Picker</span>';

    if (theme === 'auto') {
        applyTheme(window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    } else {
        applyTheme(theme);
    }
}
const applyTheme = (theme) => {
    document.documentElement.setAttribute('data-bs-theme', theme);
    document.querySelectorAll('[data-requires-theme]').forEach(element => {
        element.setAttribute(element.dataset.requiresTheme, theme);
    });
}

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

window.addEventListener('DOMContentLoaded', () => {
    picker.querySelectorAll('[data-value]').forEach(option => {
        option.addEventListener('click', e => {
            setTheme(option.dataset.value);
        });
    });
    setTheme(theme);
});