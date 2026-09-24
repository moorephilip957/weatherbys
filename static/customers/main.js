// ===== SIDEBAR TOGGLE =====
const sidebar = document.getElementById('sidebar');
const overlay = document.getElementById('sidebarOverlay');
const menuToggle = document.getElementById('menuToggle');

if (menuToggle) {
    menuToggle.addEventListener('click', () => {
        sidebar.classList.toggle('open');
        overlay.classList.toggle('active');
    });
}

if (overlay) {
    overlay.addEventListener('click', () => {
        sidebar.classList.remove('open');
        overlay.classList.remove('active');
    });
}

// ===== NOTIFICATION MODAL =====
const notifBtn = document.getElementById('notifBtn');
const notifModal = document.getElementById('notifModal');
const notifModalClose = document.getElementById('notifModalClose');

if (notifBtn) {
    notifBtn.addEventListener('click', () => {
        notifModal.classList.add('active');
    });
}

if (notifModalClose) {
    notifModalClose.addEventListener('click', () => {
        notifModal.classList.remove('active');
    });
}

if (notifModal) {
    notifModal.addEventListener('click', (e) => {
        if (e.target === notifModal) {
            notifModal.classList.remove('active');
        }
    });
}

// ===== PROFILE DROPDOWN =====
const profileChip = document.getElementById('profileChip');
const profileMenu = document.getElementById('profileMenu');

if (profileChip) {
    profileChip.addEventListener('click', (e) => {
        e.stopPropagation();
        profileMenu.classList.toggle('active');
    });
}

document.addEventListener('click', (e) => {
    if (profileMenu && !profileMenu.contains(e.target) && !profileChip.contains(e.target)) {
        profileMenu.classList.remove('active');
    }
});
