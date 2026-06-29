// Gerenciamento de progresso do aluno via localStorage
// Chave: oa_progress — { m1, m2, m3a, m3b, m3c, af } cada um: 'complete'|'in-progress'|'not-started'

const STORAGE_KEY = 'oa_progress';

const MODULES = ['m1', 'm2', 'm3a', 'm3b', 'm3c', 'af'];

function _getAll() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return {};
    return JSON.parse(raw);
  } catch {
    return {};
  }
}

function _saveAll(data) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
  } catch (e) {
    console.warn('Não foi possível salvar progresso:', e);
  }
}

export function markModuleComplete(moduleId) {
  const data = _getAll();
  data[moduleId] = 'complete';
  _saveAll(data);
  _dispatchChange(moduleId, 'complete');
}

export function markModuleStarted(moduleId) {
  const data = _getAll();
  if (data[moduleId] !== 'complete') {
    data[moduleId] = 'in-progress';
    _saveAll(data);
    _dispatchChange(moduleId, 'in-progress');
  }
}

export function getModuleStatus(moduleId) {
  const data = _getAll();
  return data[moduleId] || 'not-started';
}

export function canAccessFinal() {
  const data = _getAll();
  const required = ['m1', 'm2', 'm3a', 'm3b', 'm3c'];
  return required.every(m => data[m] === 'complete');
}

export function getProgress() {
  const data = _getAll();
  return MODULES.filter(m => data[m] === 'complete').length;
}

export function resetProgress() {
  _saveAll({});
  _dispatchChange(null, null);
}

function _dispatchChange(moduleId, status) {
  window.dispatchEvent(new CustomEvent('oa-progress-change', {
    detail: { moduleId, status, all: _getAll() }
  }));
}
