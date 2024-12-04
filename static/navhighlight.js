const navbar = document.querySelector('nav.navbar');
const links = navbar.querySelectorAll('a');

function highlightLink() {
    const path = window.location.pathname;
    for (const link of links) {
        if (link.pathname === path) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    }
}

highlightLink();