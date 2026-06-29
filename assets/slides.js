// Componente de slides reutilizável
// Uso: initSlides('container-id')
// Cada filho direto com class="slide" vira um slide.

export function initSlides(containerId) {
  const container = document.getElementById(containerId);
  if (!container) return;

  const slides = Array.from(container.querySelectorAll(':scope > .slide'));
  if (slides.length === 0) return;

  // Envolve os slides numa área
  const slideArea = document.createElement('div');
  slideArea.className = 'slides-area';
  slides.forEach(s => slideArea.appendChild(s));
  container.insertBefore(slideArea, container.firstChild);

  // Cria a barra de navegação
  const nav = document.createElement('div');
  nav.className = 'slides-nav';
  container.appendChild(nav);

  let current = 0;

  function go(idx) {
    current = Math.max(0, Math.min(idx, slides.length - 1));
    render();
  }

  function render() {
    slides.forEach((s, i) => {
      s.classList.toggle('slide-active', i === current);
      s.setAttribute('aria-hidden', i !== current ? 'true' : 'false');
    });

    // Dots
    const dots = Array.from(nav.querySelectorAll('.slide-dot'));
    dots.forEach((d, i) => d.classList.toggle('active', i === current));

    // Botões
    nav.querySelector('.slides-prev').disabled = current === 0;
    nav.querySelector('.slides-next').disabled = current === slides.length - 1;

    // Counter
    nav.querySelector('.slides-counter').textContent = `${current + 1} / ${slides.length}`;
  }

  // Montar nav
  const dotsHtml = slides.map((_, i) => `<button class="slide-dot" aria-label="Slide ${i + 1}"></button>`).join('');
  nav.innerHTML = `
    <button class="slides-prev btn-secondary btn-sm" aria-label="Slide anterior">← Anterior</button>
    <div class="slides-dots">${dotsHtml}</div>
    <span class="slides-counter"></span>
    <button class="slides-next btn-secondary btn-sm" aria-label="Próximo slide">Próximo →</button>
  `;

  nav.querySelector('.slides-prev').addEventListener('click', () => go(current - 1));
  nav.querySelector('.slides-next').addEventListener('click', () => go(current + 1));
  nav.querySelectorAll('.slide-dot').forEach((dot, i) => {
    dot.addEventListener('click', () => go(i));
  });

  // Teclado
  container.setAttribute('tabindex', '0');
  container.addEventListener('keydown', e => {
    if (e.key === 'ArrowLeft') go(current - 1);
    if (e.key === 'ArrowRight') go(current + 1);
  });

  render();
}
