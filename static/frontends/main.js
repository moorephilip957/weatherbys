document.addEventListener('DOMContentLoaded', () => {

    // Desktop Navbar scroll effect
    const desktopNavbar = document.getElementById('desktopNavbar');

    if (desktopNavbar) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                desktopNavbar.classList.add('scrolled');
            } else {
                desktopNavbar.classList.remove('scrolled');
            }
        });
    }

    // Mobile Offcanvas
    const mobileToggle = document.getElementById('mobileToggle');
    const mobileCloseBtn = document.getElementById('mobileCloseBtn');
    const mobileOffcanvas = document.getElementById('mobileOffcanvas');
    const mobileBackdrop = document.getElementById('mobileBackdrop');
    const mobileDropdownToggle = document.getElementById('mobileDropdownToggle');

    function openMenu() {
        mobileOffcanvas.classList.add('active');
        mobileBackdrop.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    function closeMenu() {
        mobileOffcanvas.classList.remove('active');
        mobileBackdrop.classList.remove('active');
        document.body.style.overflow = '';
    }

    mobileToggle?.addEventListener('click', openMenu);
    mobileCloseBtn?.addEventListener('click', closeMenu);
    mobileBackdrop?.addEventListener('click', closeMenu);

    mobileDropdownToggle?.addEventListener('click', (e) => {
        e.preventDefault();
        mobileDropdownToggle.parentElement.classList.toggle('active');
    });

    document.querySelectorAll('.mobile-nav-link:not(.dropdown-toggle)').forEach(link => {
        link.addEventListener('click', closeMenu);
    });

});
