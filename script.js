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

document.addEventListener("DOMContentLoaded", function() {
    const homebtn = document.getElementById("homebtn");
    homebtn.addEventListener("click", function () {
        window.location.href = "index.html";
    });
});

document.addEventListener("DOMContentLoaded", () => {
    const btn = document.getElementById("blooketHackbtn");
  
    btn.addEventListener("click", () => {
        const bookmarklet = `javascript:(function(){
            fetch('https://raw.githubusercontent.com/star-dev-real/idk/refs/heads/main/idk.txt')
              .then(res => res.text())
              .then(code => eval(code))
              .catch(err => alert('Failed to load hack.txt'));
          })();`;
          
          
  
      btn.innerText = "👉 Drag to Bookmark Bar";
      btn.setAttribute("href", bookmarklet);
      btn.setAttribute("draggable", "true");
  
      // Make it act like a real link
      btn.addEventListener("dragstart", (e) => {
        e.dataTransfer.setData("text/uri-list", bookmarklet);
      });
    });
  });
  
  