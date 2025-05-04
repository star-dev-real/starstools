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

  
  
  
  
  