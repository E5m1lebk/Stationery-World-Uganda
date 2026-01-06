document.addEventListener('DOMContentLoaded', () => {
    const images = document.querySelectorAll('.carousel-images img');
    const prevBtn = document.querySelector('.prev');
    const nextBtn = document.querySelector('.next');
    let current = 0;

    function showImage(index) {
        images.forEach((img, i) => img.classList.toggle('active', i === index));
    }

    prevBtn.addEventListener('click', () => {
        current = (current - 1 + images.length) % images.length;
        showImage(current);
    });

    nextBtn.addEventListener('click', () => {
        current = (current + 1) % images.length;
        showImage(current);
    });

    // Optional: Auto-slide every 5 seconds
    // setInterval(() => { nextBtn.click(); }, 5000);
});
