document.addEventListener('DOMContentLoaded', function() {
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const nav = document.querySelector('nav');
    
    if (mobileMenuBtn && nav) {
        mobileMenuBtn.addEventListener('click', function() {
            nav.classList.toggle('show');
        });
    }


    const navLinks = document.querySelectorAll('nav a');
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            nav.classList.remove('show');
        });
    });

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
                document.body.style.overflow = 'hidden'; 
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

    const contactForm = document.getElementById('contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', async function(e) {
            e.preventDefault(); 
            
            const submitBtn = contactForm.querySelector('button[type="submit"]');
            const statusEl = document.getElementById('statusContact');
            const formElements = contactForm.elements;

            submitBtn.disabled = true;
            statusEl.textContent = 'Sending message...';
            statusEl.style.color = 'var(--secondary-color)';

            try {
                const formData = {
                    name: formElements.name.value.trim(),
                    email: formElements.email.value.trim(),
                    message: formElements.message.value.trim()
                };

                if (!formData.name || !formData.email || !formData.message) {
                    throw new Error('Please fill in all required fields');
                }

                if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
                    throw new Error('Please enter a valid email address');
                }
                const response = await fetch('https://soulstools.pythonanywhere.com/api/v1/contact', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(formData)
                });

                const responseText = await response.text();
                const data = responseText ? JSON.parse(responseText) : {};

                if (!response.ok) {
                    throw new Error(data.error || `Server error: ${response.status}`);
                }

                statusEl.textContent = `Message sent successfully! ID: ${data.id}`;
                statusEl.style.color = 'var(--success-color)';
                contactForm.reset();

            } catch (error) {
                statusEl.textContent = `Error: ${error.message}`;
                statusEl.style.color = 'var(--error-color)';
                console.error('Submission error:', error);
            } finally {
                submitBtn.disabled = false;
            }
        });
    }

    const currentPage = location.pathname.split('/').pop() || 'index.html';
    const links = document.querySelectorAll('nav a');
    
    links.forEach(link => {
        if (link.getAttribute('href') === currentPage) {
            link.classList.add('active');
        }
    });
});
