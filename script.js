document.addEventListener("DOMContentLoaded", function () {
    const toolsBtn = document.getElementById("toolsbtn");

    toolsBtn.addEventListener("click", function () {
        window.location.href = "tools.html";
    });
});

document.addEventListener("DOMContentLoaded", function() {
    const creditsBtn = document.getElementById("creditsbtn");
    creditsBtn.addEventListener("click", function () {
        window.location.href = "credits.html";
    });
});

document.addEventListener("DOMContentLoaded", function () {
    const homebtns = document.getElementsByClassName("homebtn");
    Array.from(homebtns).forEach(btn => {
        btn.addEventListener("click", function () {
            window.location.href = "index.html";
        });
    });
});


document.addEventListener("DOMContentLoaded", () => {
    const btn = document.getElementById("blooketHackbtn");
  
    btn.addEventListener("click", () => {
      fetch("hack.js")
        .then(response => response.text())
        .then(data => {
          const bookmarklet = data.trim();
  
          // Create the <a> element
          const link = document.createElement("a");
          link.className = "blooketHack";
          link.innerText = "👉 Drag to Bookmark Bar";
          link.setAttribute("href", bookmarklet);
          link.setAttribute("draggable", "true");
  
          // Make it draggable to bookmark bar
          link.addEventListener("dragstart", (e) => {
            e.dataTransfer.setData("text/uri-list", bookmarklet);
          });
  
          // Replace the button with the new <a> element
          btn.replaceWith(link);
        })
        .catch(err => {
          console.error("Failed to fetch hack.js:", err);
          btn.innerText = "❌ Failed to load script";
        });
    });
  });

document.addEventListener("DOMContentLoaded", function () {
    const newsBtn = document.getElementById("newsbtn");
    newsBtn.addEventListener("click", function () {
        window.location.href = "news.html";
    });
})

document.addEventListener("DOMContentLoaded", function() {
    const contactBtn = document.getElementById("contactUsbtn");
    contactBtn.addEventListener("click", function () {
        window.location.href = "contact.html";
    })
})

document.addEventListener("DOMContentLoaded", function() {
    const submitBtn = document.getElementById("submitbtn");
    const statusLabel = document.getElementById("statusContact");

    submitBtn.addEventListener("click", function () {
        const name = document.getElementById("nameinput").value;
        const email = document.getElementById("emailinput").value;
        const message = document.getElementById("messageinput").value;

        if (name && email && message) {
            statusLabel.innerText = `Status: Thank you for your message ${name}! We will be with you shortly.`;
        } else {
            alert("Please fill out all fields.");
        }
    });
});

document.addEventListener("DOMContentLoaded", function() {
    const kahackBtn = document.getElementById("kahootHackBtn");
    kahackBtn.addEventListener("click", function () {
        window.location.href = "kahoothack.user.js";
    });
});
    

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('contact-form');
  const statusEl = document.getElementById('status');
  const submitBtn = document.querySelector('#contact-form button[type="submit"]');
  
  if (!form) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    submitBtn.disabled = true;
    statusEl.textContent = 'Sending message...';
    statusEl.style.color = 'black';

    try {
      const formData = {
        name: form.elements['name'].value.trim(),
        email: form.elements['email'].value.trim(),
        message: form.elements['message'].value.trim()
      };

      if (!formData.name || !formData.email || !formData.message) {
        throw new Error('All fields are required');
      }

      const response = await fetch('https://souuuulll.pythonanywhere.com/api/submit_contact', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: {"name": form.elements['name'].value.trim(), "email": form.elements['email'].value.trim(), "message": form.elements['message'].value.trim()}
      });

      const result = await response.json();

      if (!response.ok) {
        throw new Error(result.message || 'Submission failed');
      }

      statusEl.textContent = result.message;
      statusEl.style.color = 'green';
      form.reset();
      
      setTimeout(() => {
        statusEl.textContent = '';
      }, 5000);

    } catch (error) {
      // Error handling
      statusEl.textContent = `Error: ${error.message}`;
      statusEl.style.color = 'red';
      console.error('Submission error:', error);
    } finally {
      submitBtn.disabled = false;
    }
  });
});
