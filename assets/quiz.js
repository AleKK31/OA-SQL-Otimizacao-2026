import { markModuleComplete } from './progress.js';

// Exporta função principal — uso: initQuiz('quiz-m1', questions, 'm1')
export function initQuiz(containerId, questions, moduleId) {
  const container = document.getElementById(containerId);
  if (!container) return;

  const storageKey = `quiz_${containerId}`;
  let state = _loadState(storageKey, questions.length);

  function _loadState(key, total) {
    try {
      const raw = localStorage.getItem(key);
      if (raw) {
        const s = JSON.parse(raw);
        if (s && s.answers && s.answers.length === total) return s;
      }
    } catch {}
    return { currentIndex: 0, answers: Array(total).fill(null), completed: false };
  }

  function _saveState() {
    try {
      localStorage.setItem(storageKey, JSON.stringify(state));
    } catch {}
  }

  function _render() {
    if (state.completed) {
      _renderScore();
      return;
    }
    _renderQuestion(state.currentIndex);
  }

  function _renderQuestion(idx) {
    const q = questions[idx];
    const answered = state.answers[idx] !== null;
    const selectedIdx = state.answers[idx];

    const optionsHtml = q.options.map((opt, i) => {
      let cls = 'quiz-option';
      if (answered) {
        cls += ' disabled';
        if (i === q.correct) cls += ' correct';
        if (i === selectedIdx && i !== q.correct) cls += ' incorrect selected';
        if (i === selectedIdx && i === q.correct) cls += ' selected';
      }
      const letter = String.fromCharCode(65 + i);
      return `
        <div class="${cls}" data-idx="${i}" role="button" tabindex="${answered ? -1 : 0}">
          <span class="option-letter">${letter}</span>
          <span>${opt}</span>
        </div>
      `;
    }).join('');

    const feedbackHtml = answered ? `
      <div class="quiz-feedback ${selectedIdx === q.correct ? '' : 'incorrect'}">
        ${selectedIdx === q.correct ? '✓ Correto! ' : '✗ Incorreto. '}${q.feedback}
      </div>
    ` : '';

    const isLast = idx === questions.length - 1;
    const nextLabel = isLast ? 'Ver resultado' : 'Próxima →';
    const nextBtnHtml = answered ? `
      <button class="btn-primary quiz-next-btn btn-sm">${nextLabel}</button>
    ` : '';

    container.innerHTML = `
      <div class="quiz-card">
        <div class="quiz-progress">Pergunta ${idx + 1} de ${questions.length}</div>
        <div class="quiz-question">${q.text}</div>
        <div class="quiz-options">${optionsHtml}</div>
        ${feedbackHtml}
        <div class="quiz-actions">${nextBtnHtml}</div>
      </div>
    `;

    // Set module color CSS var if available
    const moduleColor = _getModuleColor();
    if (moduleColor) {
      container.querySelector('.quiz-card').style.setProperty('--module-color', moduleColor);
    }

    // Bind option clicks
    if (!answered) {
      container.querySelectorAll('.quiz-option').forEach(el => {
        el.addEventListener('click', () => _answerQuestion(idx, parseInt(el.dataset.idx)));
        el.addEventListener('keydown', e => {
          if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            _answerQuestion(idx, parseInt(el.dataset.idx));
          }
        });
      });
    }

    // Bind next button
    const nextBtn = container.querySelector('.quiz-next-btn');
    if (nextBtn) {
      nextBtn.addEventListener('click', () => {
        if (idx + 1 >= questions.length) {
          state.completed = true;
          _saveState();
          if (moduleId) markModuleComplete(moduleId);
          _renderScore();
        } else {
          state.currentIndex = idx + 1;
          _saveState();
          _renderQuestion(state.currentIndex);
        }
      });
    }
  }

  function _answerQuestion(idx, selectedIdx) {
    state.answers[idx] = selectedIdx;
    _saveState();
    _renderQuestion(idx);
  }

  function _renderScore() {
    const correct = state.answers.filter((ans, i) => ans === questions[i].correct).length;
    const total = questions.length;
    const pct = Math.round((correct / total) * 100);

    const moduleColor = _getModuleColor() || '#534AB7';

    container.innerHTML = `
      <div class="quiz-card">
        <div class="quiz-score">
          <div class="score-number" style="color:${moduleColor}">${correct}/${total}</div>
          <div class="score-label">${pct >= 70 ? '🎉 Bom resultado!' : '📚 Revise os conceitos e tente novamente.'}</div>
          <div class="text-muted text-sm mb-3">${pct}% de acertos</div>
          <button class="btn-secondary btn-sm quiz-retry-btn">↺ Refazer quiz</button>
        </div>
      </div>
    `;

    container.querySelector('.quiz-retry-btn').addEventListener('click', () => {
      state = { currentIndex: 0, answers: Array(questions.length).fill(null), completed: false };
      _saveState();
      _render();
    });
  }

  function _getModuleColor() {
    const style = getComputedStyle(document.documentElement);
    return style.getPropertyValue('--module-color').trim() || null;
  }

  _render();
}
