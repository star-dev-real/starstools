document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu toggle
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const nav = document.querySelector('nav');
    
    if (mobileMenuBtn && nav) {
        mobileMenuBtn.addEventListener('click', function() {
            nav.classList.toggle('show');
        });
    }

    // Close mobile menu when clicking a link
    const navLinks = document.querySelectorAll('nav a');
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            nav.classList.remove('show');
        });
    });

    // Tool purchase modal
    const purchaseBtns = document.querySelectorAll('.purchase-btn');
    const modal = document.getElementById('purchase-modal');
    const modalToolName = document.getElementById('modal-tool-name');
    const modalToolPrice = document.getElementById('modal-tool-price');
    const closeModal = document.querySelector('.close-modal');

    if (purchaseBtns.length && modal) {
        purchaseBtns.forEach(btn => {
            btn.addEventListener('click', function() {
                const toolName = this.getAttribute('data-tool');
                const toolPrice = this.parentElement.querySelector('.tool-price').textContent;
                
                modalToolName.textContent = toolName;
                modalToolPrice.textContent = toolPrice;
                modal.style.display = 'flex';
                document.body.style.overflow = 'hidden'; // Prevent scrolling when modal is open
            });
        });

        closeModal.addEventListener('click', function() {
            modal.style.display = 'none';
            document.body.style.overflow = 'auto';
        });

        window.addEventListener('click', function(e) {
            if (e.target === modal) {
                modal.style.display = 'none';
                document.body.style.overflow = 'auto';
            }
        });
    }

    // Contact form handling
    const contactForm = document.getElementById('contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const submitBtn = contactForm.querySelector('button[type="submit"]');
            const statusEl = document.getElementById('statusContact');
            
            submitBtn.disabled = true;
            statusEl.textContent = 'Sending message...';
            statusEl.style.color = 'var(--secondary-color)';
            
            try {
                const formData = {
                    name: contactForm.elements['name'].value.trim(),
                    email: contactForm.elements['email'].value.trim(),
                    message: contactForm.elements['message'].value.trim()
                };

                // Basic validation
                if (!formData.name || !formData.email || !formData.message) {
                    throw new Error('All fields are required');
                }

                if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
                    throw new Error('Please enter a valid email address');
                }

                // In a real implementation, you would send this to your server
                // For now, we'll simulate a successful submission
                await new Promise(resolve => setTimeout(resolve, 1000));
                
                statusEl.textContent = 'Message sent successfully! We will contact you soon.';
                statusEl.style.color = 'var(--success-color)';
                contactForm.reset();
            } catch (error) {
                statusEl.textContent = `Error: ${error.message}`;
                statusEl.style.color = 'var(--error-color)';
            } finally {
                submitBtn.disabled = false;
            }
        });
    }

    // Add active class to current page link
    const currentPage = location.pathname.split('/').pop() || 'index.html';
    const links = document.querySelectorAll('nav a');
    
    links.forEach(link => {
        if (link.getAttribute('href') === currentPage) {
            link.classList.add('active');
        }
    });
});