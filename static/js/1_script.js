document.addEventListener('DOMContentLoaded', () => {

    // =================================================================
    // 1. CORE NAVIGATION & LAYOUT
    // =================================================================

    // --- Smooth Scrolling for anchor links ---
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });

    // --- Navbar Scroll Effect ---
    const navbar = document.getElementById('navbar');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // --- Active Nav Link on Scroll ---
    const sections = document.querySelectorAll('main > section');
    const navLinks = document.querySelectorAll('.nav-link');
    const navObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const id = entry.target.id;
                navLinks.forEach(link => {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === `#${id}`) {
                        link.classList.add('active');
                    }
                });
            }
        });
    }, { rootMargin: '-50% 0px -50% 0px' });
    sections.forEach(section => navObserver.observe(section));


    // =================================================================
    // 2. TABS & FILTERING LOGIC
    // =================================================================

    // --- Main Skills Tabs (Tech Stack / Expertise) ---
    const tabs = document.querySelectorAll('.tab-btn');
    const panels = document.querySelectorAll('.skills-panel');
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const target = document.querySelector(tab.dataset.target);
            tabs.forEach(t => t.classList.remove('active'));
            panels.forEach(p => p.classList.remove('active'));
            tab.classList.add('active');
            target.classList.add('active');
        });
    });

    // --- Tech Stack Sub-Tab Filtering ---
    const subTabBtns = document.querySelectorAll('.sub-tab-btn');
    const skillCards = document.querySelectorAll('.skills-grid .skill-card');
    const filterSkills = (category) => {
        subTabBtns.forEach(btn => {
            btn.classList.toggle('active', btn.dataset.category === category);
        });
        skillCards.forEach(card => {
            const cardCategory = card.dataset.category;
            const shouldShow = category === 'all' || cardCategory === category;
            card.classList.toggle('hide', !shouldShow);
        });
    };
    subTabBtns.forEach(btn => {
        btn.addEventListener('click', () => filterSkills(btn.dataset.category));
    });

    // --- Project Filtering ---
    const projectFilterBtns = document.querySelectorAll('.project-filters .filter-btn');
    const projectCards = document.querySelectorAll('.all-projects-grid .project-card');
    const filterProjects = (filter) => {
        projectFilterBtns.forEach(btn => {
            btn.classList.toggle('active', btn.dataset.filter === filter);
        });
        projectCards.forEach(card => {
            const cardCategories = card.dataset.category.split(' ');
            const shouldShow = filter === 'all' || cardCategories.includes(filter);
            card.classList.toggle('hide', !shouldShow);
        });
    };
    projectFilterBtns.forEach(btn => {
        btn.addEventListener('click', () => filterProjects(btn.dataset.filter));
    });
    filterProjects('featured');

    // --- License Filtering ---
    const licenseFilterBtns = document.querySelectorAll('.license-filters .filter-btn');
    const licenseCards = document.querySelectorAll('.licenses-grid .license-card');
    const filterLicenses = (filter) => {
        licenseFilterBtns.forEach(btn => {
            btn.classList.toggle('active', btn.dataset.filter === filter);
        });
        licenseCards.forEach(card => {
            const cardCategories = card.dataset.category.split(' ');
            const shouldShow = filter === 'all' || cardCategories.includes(filter);
            card.classList.toggle('hide', !shouldShow);
        });
    };
    licenseFilterBtns.forEach(btn => {
        btn.addEventListener('click', () => filterLicenses(btn.dataset.filter));
    });
    filterLicenses('all');

    // --- Expertise to Project Link Logic ---
    const expertiseLinks = document.querySelectorAll('.expertise-link');
    expertiseLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const filterTarget = link.dataset.filterTarget;
            document.getElementById('all-projects')?.scrollIntoView({ behavior: 'smooth' });
            filterProjects(filterTarget);
        });
    });


    // =================================================================
    // 3. DYNAMIC & INTERACTIVE EFFECTS
    // =================================================================

    // --- Mobile Navigation (Hamburger Menu) ---
    const mobileNavToggle = document.querySelector('.mobile-nav-toggle');
    const navMenu = document.querySelector('.nav-menu');
    const navMenuLinks = document.querySelectorAll('.nav-menu a');
    const toggleMenu = () => {
        // [FIX] This line was missing from your file. It enables the background blur.
        document.body.classList.toggle('nav-open');

        navMenu.classList.toggle('is-active');
        mobileNavToggle.classList.toggle('is-active');
        const icon = mobileNavToggle.querySelector('i');
        if (navMenu.classList.contains('is-active')) {
            icon.classList.replace('bi-list', 'bi-x');
        } else {
            icon.classList.replace('bi-x', 'bi-list');
        }
    };
    mobileNavToggle.addEventListener('click', toggleMenu);
    navMenuLinks.forEach(link => {
        link.addEventListener('click', () => {
            if (navMenu.classList.contains('is-active')) {
                toggleMenu();
            }
        });
    });

    // --- Section Scanner Reveal ---
    const sectionHeaders = document.querySelectorAll('.section-header');
    const scannerObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('scanned');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.3 });
    sectionHeaders.forEach(header => scannerObserver.observe(header));

    // --- Interactive Card Spotlight ---
    const spotlightCards = document.querySelectorAll('.skill-card, .expertise-card, .cert-card, .project-card');
    spotlightCards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            card.style.setProperty('--mouse-x', `${e.clientX - rect.left}px`);
            card.style.setProperty('--mouse-y', `${e.clientY - rect.top}px`);
        });
    });

    // --- General Scroll-In Animation ---
    // [FIX] This now only targets '.stat-item' to prevent bugs with card filtering.
    const statItems = document.querySelectorAll('.stat-item');
    const animateOnScroll = () => {
        statItems.forEach(element => {
            if (element.getBoundingClientRect().top < window.innerHeight - 50) {
                element.style.opacity = '1';
                element.style.transform = 'translateY(0)';
            }
        });
    };
    statItems.forEach(element => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(30px)';
        element.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    });
    window.addEventListener('scroll', animateOnScroll);
    animateOnScroll();

});