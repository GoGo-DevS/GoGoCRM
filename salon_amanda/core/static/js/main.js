/* ============================================================
   Salón Amanda — main.js
   Desarrollado por GoGoDevS
============================================================ */

'use strict';

/* ============================================================
   NAVBAR — cambio de estilo al hacer scroll
============================================================ */
const navbar = document.getElementById('mainNavbar');

function handleNavbarScroll() {
    navbar.classList.toggle('scrolled', window.scrollY > 60);
}

window.addEventListener('scroll', handleNavbarScroll, { passive: true });
handleNavbarScroll();


/* ============================================================
   CERRAR MENÚ MOBILE AL HACER CLICK EN UN LINK
============================================================ */
const navbarCollapse = document.getElementById('navbarNav');

document.querySelectorAll('#navbarNav .nav-link').forEach(link => {
    link.addEventListener('click', () => {
        if (navbarCollapse && navbarCollapse.classList.contains('show')) {
            const bsCollapse = bootstrap.Collapse.getInstance(navbarCollapse);
            if (bsCollapse) bsCollapse.hide();
        }
    });
});


/* ============================================================
   SCROLL REVEAL — Intersection Observer
   Delay escalonado en cards: 0, 100, 200 ms...
============================================================ */
const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (!entry.isIntersecting) return;

        const el = entry.target;
        const parent = el.parentElement;

        const siblings = Array.from(parent.querySelectorAll(':scope > .reveal:not(.revealed)'));

        if (siblings.length > 1) {
            siblings.forEach((sibling, i) => {
                setTimeout(() => {
                    sibling.classList.add('revealed');
                    revealObserver.unobserve(sibling);
                }, i * 100);
            });
        } else {
            el.classList.add('revealed');
            revealObserver.unobserve(el);
        }
    });
}, {
    threshold: 0.15,
    rootMargin: '0px 0px -40px 0px'
});

document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));


/* ============================================================
   NAV LINK ACTIVO SEGÚN SECCIÓN VISIBLE
============================================================ */
const allNavLinks = document.querySelectorAll('.navbar-nav .nav-link[href^="#"]');

const sectionObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        allNavLinks.forEach(link => link.classList.remove('active'));
        const activeLink = document.querySelector(
            `.navbar-nav .nav-link[href="#${entry.target.id}"]`
        );
        if (activeLink) activeLink.classList.add('active');
    });
}, {
    threshold: 0.35,
    rootMargin: `-68px 0px -45% 0px`
});

document.querySelectorAll('section[id]').forEach(section => sectionObserver.observe(section));


/* ============================================================
   SMOOTH SCROLL para anclas internas
============================================================ */
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        if (href === '#') return;
        const target = document.querySelector(href);
        if (!target) return;
        e.preventDefault();
        const offsetTop = target.getBoundingClientRect().top + window.scrollY - 68;
        window.scrollTo({ top: offsetTop, behavior: 'smooth' });
    });
});
