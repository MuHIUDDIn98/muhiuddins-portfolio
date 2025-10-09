/**
 * Main application script for the portfolio website.
 * Initializes all interactive components after the DOM is fully loaded.
 */
document.addEventListener("DOMContentLoaded", main);

function main() {
  /**
   * Centralized object for DOM element selections for performance and maintainability.
   */
  const elements = {
    navbar: document.getElementById("navbar"),
    navLinks: document.querySelectorAll(".nav-link"),
    mobileNavToggle: document.querySelector(".mobile-nav-toggle"),
    navMenu: document.querySelector(".nav-menu"),
    allSections: document.querySelectorAll("main > section"),
    sectionHeaders: document.querySelectorAll(".section-header"),
    spotlightCards: document.querySelectorAll(".skill-card, .expertise-card, .project-card, .contact-card"),
    statItems: document.querySelectorAll(".stat-item"),
    skillTabsContainer: document.querySelector(".skills-tabs"),
    skillPanels: document.querySelectorAll(".skills-panel"),
    subTabsContainer: document.querySelector(".skills-sub-tabs"),
    skillCards: document.querySelectorAll(".skills-grid .skill-card"),
    projectFiltersContainer: document.querySelector(".project-filters"),
    projectCards: document.querySelectorAll(".all-projects-grid .project-card"),
    contactForm: document.querySelector(".contact-form"),
    formContainer: document.getElementById("form-container"),
    successMessage: document.getElementById("success-message"),
    typewriterElement: document.getElementById("typewriter-title"),
    contactSection: document.getElementById('contact'),
    gradientsContainer: document.querySelector(".gradients-container"),
    emailTrackButton: document.getElementById("track-email-click"),
  };

  /**
   * Sets up core navigation features: smooth scrolling, scroll effects, and mobile menu.
   */
  const initNavigation = () => {
    // Smooth Scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener("click", function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute("href"))?.scrollIntoView({ behavior: "smooth" });
      });
    });

    // Navbar scroll effect
    window.addEventListener("scroll", () => {
      elements.navbar?.classList.toggle("scrolled", window.scrollY > 50);
    });

    // Mobile Navigation
    if (elements.mobileNavToggle && elements.navMenu) {
      const toggleMenu = () => {
        document.body.classList.toggle("nav-open");
        elements.navMenu.classList.toggle("is-active");
        const icon = elements.mobileNavToggle.querySelector("i");
        icon.classList.toggle("bi-list");
        icon.classList.toggle("bi-x");
      };
      elements.mobileNavToggle.addEventListener("click", toggleMenu);
      elements.navMenu.querySelectorAll("a").forEach(link => {
        link.addEventListener("click", () => {
          if (elements.navMenu.classList.contains("is-active")) toggleMenu();
        });
      });
    }
  };
  
  /**
   * Initializes all content filtering using event delegation.
   */
  const initFiltering = () => {
    // Main Skills Tabs (Tech Stack / Expertise)
    elements.skillTabsContainer?.addEventListener("click", e => {
        if (!e.target.matches(".tab-btn")) return;
        elements.skillTabsContainer.querySelectorAll(".tab-btn").forEach(t => t.classList.remove("active"));
        e.target.classList.add("active");
        elements.skillPanels.forEach(p => p.classList.remove("active"));
        document.querySelector(e.target.dataset.target)?.classList.add("active");
    });

    const setupFilter = (container, buttonSelector, cards, dataAttribute) => {
        if (!container) return;
        container.addEventListener('click', e => {
            if (!e.target.matches(buttonSelector)) return;
            const filter = e.target.dataset[dataAttribute];
            container.querySelectorAll(buttonSelector).forEach(btn => btn.classList.remove('active'));
            e.target.classList.add('active');
            cards.forEach(card => {
                const categories = card.dataset.category?.split(' ') || [];
                const shouldShow = filter === 'all' || categories.includes(filter);
                card.classList.toggle('hide', !shouldShow);
            });
        });
    };
    
    setupFilter(elements.subTabsContainer, '.sub-tab-btn', elements.skillCards, 'category');
    setupFilter(elements.projectFiltersContainer, '.filter-btn', elements.projectCards, 'filter');
    
    // Set initial states
    elements.subTabsContainer?.querySelector('[data-category="all"]')?.click();
    elements.projectFiltersContainer?.querySelector('[data-filter="featured"]')?.click();
  };
  
  /**
   * Initializes scroll-based animations and interactive mouse-move effects.
   */
  const initAnimationsAndEffects = () => {
    const observer = new IntersectionObserver((entries, obs) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add("in-view");
          obs.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15 });

    elements.statItems.forEach(item => observer.observe(item));
    elements.sectionHeaders.forEach(header => {
        // Renaming in-view to scanned for this specific element to trigger the right animation
        header.addEventListener('in-view', () => header.classList.add('scanned'), { once: true });
        observer.observe(header);
    });
    
    const navObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          elements.navLinks.forEach(link => {
            link.classList.toggle("active", link.getAttribute("href") === `#${entry.target.id}`);
          });
        }
      });
    }, { rootMargin: "-40% 0px -60% 0px" });
    elements.allSections.forEach(section => navObserver.observe(section));
    
    elements.spotlightCards.forEach(card => {
      card.addEventListener("mousemove", e => {
        const rect = card.getBoundingClientRect();
        card.style.setProperty("--mouse-x", `${e.clientX - rect.left}px`);
        card.style.setProperty("--mouse-y", `${e.clientY - rect.top}px`);
      });
    });

    if (elements.gradientsContainer) {
      window.addEventListener("mousemove", (e) => {
        const { clientX, clientY } = e;
        const x = (clientX / window.innerWidth) * 2 - 1;
        const y = (clientY / window.innerHeight) * 2 - 1;
        elements.gradientsContainer.style.transform = `translate(${-x * 30}px, ${-y * 30}px)`;
      });
    }
  };
  
  /**
   * Initializes all contact form functionality.
   */
  const initContactForm = () => {
    if (!elements.contactForm) return;

    if (elements.successMessage) {
      elements.formContainer.style.display = "none";
      elements.successMessage.style.display = "flex";
    }

    if (elements.typewriterElement && elements.contactSection) {
      const text = elements.typewriterElement.innerText;
      elements.typewriterElement.innerText = '';
      const type = (i = 0) => {
        if (i < text.length) {
          elements.typewriterElement.innerHTML += text.charAt(i);
          setTimeout(() => type(i + 1), 100);
        }
      };
      new IntersectionObserver((entries, obs) => {
        if (entries[0].isIntersecting) {
          setTimeout(type, 500);
          obs.disconnect();
        }
      }, { threshold: 0.6 }).observe(elements.contactSection);
    }
    
    const requiredInputs = elements.contactForm.querySelectorAll("[required]");
    const validateInput = input => {
        const formGroup = input.closest(".form-group");
        const errorEl = formGroup.querySelector(".error-message");
        const isValid = input.checkValidity();
        formGroup.classList.toggle("invalid", !isValid);
        if (errorEl) errorEl.textContent = input.validationMessage;
        return isValid;
    };

    elements.contactForm.addEventListener("submit", e => {
      const isFormValid = [...requiredInputs].every(input => validateInput(input));
      if (!isFormValid) e.preventDefault();
    });

    requiredInputs.forEach(input => {
      input.addEventListener("input", () => validateInput(input));
    });
  };

  /**
   * Initializes simple analytics like click tracking.
   */
  const initAnalytics = () => {
    if (elements.emailTrackButton) {
        elements.emailTrackButton.addEventListener("click", () => {
            const trackUrl = "/track_click/?action=EMAIL_CLICK";
            if (navigator.sendBeacon) {
                navigator.sendBeacon(trackUrl);
            } else {
                fetch(trackUrl, { method: "GET", keepalive: true });
            }
        });
    }
  };

  // Run all initialization modules
  initNavigation();
  initFiltering();
  initAnimationsAndEffects();
  initContactForm();
  initAnalytics();
}