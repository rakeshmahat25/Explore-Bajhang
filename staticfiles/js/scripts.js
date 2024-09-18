document.addEventListener("DOMContentLoaded", function() {
    // Smooth Scroll
    const scrollLinks = document.querySelectorAll(".nav-link");

    scrollLinks.forEach(link => {
        link.addEventListener("click", function(e) {
            e.preventDefault();
            const targetId = this.getAttribute("href").substring(1);
            const targetSection = document.getElementById(targetId);
            targetSection.scrollIntoView({
                behavior: "smooth"
            });
        });
    });

    // Scroll animations
    const sections = document.querySelectorAll("section");

    window.addEventListener("scroll", function() {
        const scrollPosition = window.scrollY;

        sections.forEach(section => {
            if (scrollPosition >= section.offsetTop - 500) {
                section.style.opacity = "1";
                section.style.transform = "translateY(0)";
            } else {
                section.style.opacity = "0";
                section.style.transform = "translateY(50px)";
            }
        });
    });
});


var script = document.createElement('script');
script.id = 'chatbotscript';
script.dataset.accountid = 'KnvtBJmzDEwN/SD0R5JWog==';
script.dataset.websiteid = 'yUbl/JhM2rIpBzVHnJR6Hg==';
script.src = 'https://app.robofy.ai/bot/js/common.js?v='+ new Date().getTime(); document.head.appendChild(script);



document.addEventListener('DOMContentLoaded', function() {
    const section = document.getElementById('about');
    const images = [
        '{% static 'images/bajhang.jpg' %}',
        '{% static 'images/Namaste1.jpg' %}'
//        '{% static 'images/bajhang3.jpg' %}'
    ];
    let currentIndex = 0;

    function changeBackgroundImage() {
        currentIndex = (currentIndex + 1) % images.length;
        section.style.backgroundImage = `url('${images[currentIndex]}')`;
    }

    setInterval(changeBackgroundImage, 10000); // Change image every 10 seconds
});