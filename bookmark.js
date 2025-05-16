javascript:(() => {
    const num = 100; 
    const originalUrl = window.location.href;
    const colors = ['#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#FF00FF', '#00FFFF'];
    let colorIndex = 0;
    
    function executeBoth() {
        for (let i = 1; i <= num; i++) {
            history.pushState(null, null, i === num ? originalUrl : `/${i}`);
        }
        
        const flash = () => {
            document.body.style.backgroundColor = colors[colorIndex];
            colorIndex = (colorIndex + 1) % colors.length;
            requestAnimationFrame(flash);
        };
        flash();
    }

    executeBoth();
})();