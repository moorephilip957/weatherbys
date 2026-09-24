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

// ===== CHART =====
const cashflowCanvas = document.getElementById('cashflowChart');
if (cashflowCanvas) {
    const ctx = cashflowCanvas.getContext('2d');
    const grad1 = ctx.createLinearGradient(0, 0, 0, 240);
    grad1.addColorStop(0, 'rgba(91,91,247,0.25)');
    grad1.addColorStop(1, 'rgba(91,91,247,0)');
    const grad2 = ctx.createLinearGradient(0, 0, 0, 240);
    grad2.addColorStop(0, 'rgba(0,212,168,0.2)');
    grad2.addColorStop(1, 'rgba(0,212,168,0)');

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Sep 1','Sep 4','Sep 7','Sep 10','Sep 13','Sep 16','Sep 19','Sep 22','Sep 24'],
            datasets: [
                {
                    label: 'Income',
                    data: [1200, 1800, 1400, 2400, 2100, 2800, 3200, 3600, 4200],
                    borderColor: '#5B5BF7',
                    backgroundColor: grad1,
                    borderWidth: 2.5,
                    fill: true,
                    tension: 0.4,
                    pointRadius: 0,
                    pointHoverRadius: 6,
                    pointHoverBackgroundColor: '#5B5BF7',
                    pointHoverBorderColor: '#fff',
                    pointHoverBorderWidth: 3,
                },
                {
                    label: 'Expenses',
                    data: [800, 1200, 900, 1400, 1100, 1600, 1800, 2200, 3180],
                    borderColor: '#00D4A8',
                    backgroundColor: grad2,
                    borderWidth: 2.5,
                    fill: true,
                    tension: 0.4,
                    pointRadius: 0,
                    pointHoverRadius: 6,
                    pointHoverBackgroundColor: '#00D4A8',
                    pointHoverBorderColor: '#fff',
                    pointHoverBorderWidth: 3,
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: '#0A0E1A',
                    padding: 12,
                    titleFont: { size: 12, weight: '600' },
                    bodyFont: { size: 12 },
                    cornerRadius: 10,
                    displayColors: true,
                    boxPadding: 4,
                    callbacks: {
                        label: c => ` ${c.dataset.label}: $${c.parsed.y.toLocaleString()}`
                    }
                }
            },
            scales: {
                x: {
                    grid: { display: false },
                    ticks: { color: '#9CA3AF', font: { size: 11 }, maxRotation: 0 },
                    border: { display: false }
                },
                y: {
                    grid: { color: '#F3F4F8', drawBorder: false },
                    ticks: {
                        color: '#9CA3AF',
                        font: { size: 11 },
                        callback: v => '$' + (v/1000) + 'k',
                        maxTicksLimit: 5
                    },
                    border: { display: false }
                }
            },
            interaction: { mode: 'index', intersect: false }
        }
    });
}

// ===== 3D CARD TILT =====
const card3d = document.getElementById('card3d');
if (card3d && window.matchMedia('(hover: hover)').matches) {
    card3d.addEventListener('mousemove', e => {
        const r = card3d.getBoundingClientRect();
        const x = e.clientX - r.left;
        const y = e.clientY - r.top;
        const rx = ((y / r.height) - 0.5) * -12;
        const ry = ((x / r.width) - 0.5) * 12;
        card3d.style.transform = `rotateX(${rx}deg) rotateY(${ry}deg)`;
    });
    card3d.addEventListener('mouseleave', () => {
        card3d.style.transform = 'rotateX(0) rotateY(0)';
    });
}

// ===== CHART TABS =====
document.querySelectorAll('.chart-tabs button').forEach(b => {
    b.addEventListener('click', () => {
        document.querySelectorAll('.chart-tabs button').forEach(x => x.classList.remove('active'));
        b.classList.add('active');
    });
});

// ===== CARD DOTS =====
document.querySelectorAll('.card-dots .d').forEach(dot => {
    dot.addEventListener('click', () => {
        document.querySelectorAll('.card-dots .d').forEach(d => d.classList.remove('active'));
        dot.classList.add('active');
    });
});