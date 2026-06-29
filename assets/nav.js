import { getModuleStatus, canAccessFinal } from './progress.js';

const MODULE_SEQUENCE = ['m1', 'm2', 'm3a', 'm3b', 'm3c', 'af'];

const MODULE_INFO = {
  m1:  { label: '1',   name: 'Entendendo o Problema',        color: '#534AB7', href: '../m1/' },
  m2:  { label: '2',   name: 'Diagnóstico',                  color: '#0F6E56', href: '../m2/' },
  m3a: { label: '3.1', name: 'Índices',                      color: '#185FA5', href: '../m3a/' },
  m3b: { label: '3.2', name: 'Reescrita de Consulta',        color: '#993C1D', href: '../m3b/' },
  m3c: { label: '3.3', name: 'Infraestrutura e Manutenção',  color: '#993556', href: '../m3c/' },
  af:  { label: '4',   name: 'Avaliação Final',              color: '#3B6D11', href: '../af/' },
};

export function initNav(currentModuleId) {
  const container = document.getElementById('module-nav');
  if (!container) return;

  const currentIdx = MODULE_SEQUENCE.indexOf(currentModuleId);
  const nextModuleId = MODULE_SEQUENCE[currentIdx + 1] || null;

  // Build inner HTML
  const pills = MODULE_SEQUENCE.map(id => {
    const info = MODULE_INFO[id];
    const status = getModuleStatus(id);
    const isActive = id === currentModuleId;
    const isAF = id === 'af';
    const isLocked = isAF && !canAccessFinal();
    const isComplete = status === 'complete';

    let label = info.label;
    if (isComplete) label = '✓ ' + label;
    if (isLocked) label = '🔒 ' + label;

    const classes = [
      'nav-pill',
      isActive ? 'active' : '',
      isComplete && !isActive ? 'complete' : '',
      isLocked ? 'locked' : '',
    ].filter(Boolean).join(' ');

    const style = isActive
      ? `background:${info.color}; color:#fff;`
      : isComplete
        ? `color:${info.color}; border-color:${info.color};`
        : '';

    if (isLocked) {
      return `<button class="${classes}" data-locked="true" data-module="${id}" style="${style}" title="${info.name}">${label}</button>`;
    }

    return `<a class="${classes}" href="${info.href}" style="${style}" title="${info.name}">${label}</a>`;
  }).join('');

  const nextBtn = nextModuleId
    ? `<a href="${MODULE_INFO[nextModuleId].href}" class="nav-next-btn">→ Próximo</a>`
    : '';

  container.innerHTML = `
    <div class="nav-inner">
      <a href="../index.html" class="nav-home-btn">← Início</a>
      <span class="nav-sep">|</span>
      <div class="nav-pills">${pills}</div>
      ${nextBtn}
    </div>
  `;

  // Toast for locked AF
  let toastEl = document.getElementById('nav-toast');
  if (!toastEl) {
    toastEl = document.createElement('div');
    toastEl.id = 'nav-toast';
    toastEl.className = 'toast';
    document.body.appendChild(toastEl);
  }

  container.querySelectorAll('[data-locked="true"]').forEach(btn => {
    btn.addEventListener('click', () => {
      toastEl.textContent = 'Complete todos os módulos antes de acessar a Avaliação Final.';
      toastEl.classList.add('show');
      setTimeout(() => toastEl.classList.remove('show'), 3000);
    });
  });

  // Re-render on progress changes
  window.addEventListener('oa-progress-change', () => initNav(currentModuleId));
}
