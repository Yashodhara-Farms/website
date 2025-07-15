// hero.js
const slides = document.querySelector('#carousel-slides');
const dots = document.querySelectorAll('#carousel-dots button');
const totalSlides = dots.length;
let current = 0;
let interval;

function updateCarousel(index) {
  slides.style.transform = `translateX(-${index * 100}%)`;
  dots.forEach((dot, i) => {
    dot.classList.toggle('opacity-70', i === index);
    dot.classList.toggle('opacity-30', i !== index);
  });
  current = index;
}

function nextSlide() {
  updateCarousel((current + 1) % totalSlides);
}

function prevSlide() {
  updateCarousel((current - 1 + totalSlides) % totalSlides);
}

function startAutoSlide() {
  interval = setInterval(nextSlide, 10000);
}

function stopAutoSlide() {
  clearInterval(interval);
}

document.getElementById('next').addEventListener('click', () => {
  stopAutoSlide();
  nextSlide();
  startAutoSlide();
});

document.getElementById('prev').addEventListener('click', () => {
  stopAutoSlide();
  prevSlide();
  startAutoSlide();
});

dots.forEach(dot => {
  dot.addEventListener('click', () => {
    stopAutoSlide();
    updateCarousel(parseInt(dot.dataset.index));
    startAutoSlide();
  });
});

updateCarousel(0);
startAutoSlide();
