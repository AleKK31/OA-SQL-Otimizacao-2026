// Componente reutilizável de editor SQL com PGLite (PostgreSQL em WebAssembly)
// Uso: initPGLite(containerId, seedSQL, exerciseSQL)

const PGLITE_CDN = 'https://cdn.jsdelivr.net/npm/@electric-sql/pglite/dist/index.js';

// Cache de instâncias PGLite por containerId
const _dbInstances = {};
// Cache do módulo importado
let _pgliteModule = null;

async function _loadPGLite() {
  if (_pgliteModule) return _pgliteModule;
  _pgliteModule = await import(PGLITE_CDN);
  return _pgliteModule;
}

async function _getDB(containerId, seedSQL) {
  if (_dbInstances[containerId]) return _dbInstances[containerId];

  const { PGlite } = await _loadPGLite();
  const db = new PGlite();
  await db.waitReady;

  if (seedSQL && seedSQL.trim()) {
    try {
      await db.exec(seedSQL);
    } catch (e) {
      console.error(`[PGLite:${containerId}] Seed error:`, e);
    }
  }

  _dbInstances[containerId] = db;
  return db;
}

export async function initPGLite(containerId, seedSQL, exerciseSQL) {
  const container = document.getElementById(containerId);
  if (!container) {
    console.warn(`[PGLite] Container #${containerId} não encontrado.`);
    return;
  }

  // Render skeleton
  container.innerHTML = `
    <div class="sql-editor-wrapper" id="${containerId}-wrapper">
      <div class="sql-editor-header">
        <span class="sql-editor-title">Editor SQL · PGLite</span>
        <div class="sql-editor-actions">
          <button class="btn-reset" id="${containerId}-reset-btn" title="Resetar para o SQL inicial">↺ Resetar</button>
          <button class="btn-run" id="${containerId}-run-btn">▶ Executar</button>
        </div>
      </div>
      <textarea
        class="sql-editor"
        id="${containerId}-textarea"
        spellcheck="false"
        autocomplete="off"
        autocorrect="off"
        autocapitalize="off"
      >${exerciseSQL || ''}</textarea>
      <div class="sql-result" id="${containerId}-result">
        <div class="sql-loading" id="${containerId}-loading">⏳ Inicializando banco de dados...</div>
      </div>
    </div>
  `;

  const textarea = document.getElementById(`${containerId}-textarea`);
  const resultEl = document.getElementById(`${containerId}-result`);
  const runBtn = document.getElementById(`${containerId}-run-btn`);
  const resetBtn = document.getElementById(`${containerId}-reset-btn`);
  const loadingEl = document.getElementById(`${containerId}-loading`);

  // Support Tab key inside textarea
  textarea.addEventListener('keydown', e => {
    if (e.key === 'Tab') {
      e.preventDefault();
      const start = textarea.selectionStart;
      const end = textarea.selectionEnd;
      textarea.value = textarea.value.substring(0, start) + '  ' + textarea.value.substring(end);
      textarea.selectionStart = textarea.selectionEnd = start + 2;
    }
  });

  // Init DB
  let db;
  try {
    db = await _getDB(containerId, seedSQL);
    loadingEl.remove();
    _showEmpty(resultEl);
  } catch (err) {
    _showError(resultEl, `Erro ao inicializar PGLite: ${err.message}`);
    runBtn.disabled = true;
    return;
  }

  // Run button
  runBtn.addEventListener('click', () => _runQuery());

  // Ctrl+Enter shortcut
  textarea.addEventListener('keydown', e => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
      e.preventDefault();
      _runQuery();
    }
  });

  // Reset button
  resetBtn.addEventListener('click', () => {
    textarea.value = exerciseSQL || '';
    _showEmpty(resultEl);
  });

  async function _runQuery() {
    const sql = textarea.value.trim();
    if (!sql) return;

    runBtn.disabled = true;
    runBtn.textContent = '⏳ Executando...';
    resultEl.innerHTML = '<div class="sql-loading">Executando...</div>';

    const t0 = performance.now();
    try {
      // Execute all statements (split on semicolons, filter empty)
      const stmts = _splitStatements(sql);
      let lastResult = null;
      for (const stmt of stmts) {
        if (stmt.trim()) {
          lastResult = await db.query(stmt);
        }
      }
      const elapsed = (performance.now() - t0).toFixed(1);
      _showResult(resultEl, lastResult, elapsed);
    } catch (err) {
      const elapsed = (performance.now() - t0).toFixed(1);
      _showError(resultEl, err.message, elapsed);
    } finally {
      runBtn.disabled = false;
      runBtn.textContent = '▶ Executar';
    }
  }
}

function _splitStatements(sql) {
  // Simple split — handles most cases; skips single-line comments
  const lines = sql.split('\n').filter(l => !l.trim().startsWith('--'));
  const cleaned = lines.join('\n');
  return cleaned.split(';').map(s => s.trim()).filter(Boolean);
}

function _showResult(container, result, elapsed) {
  if (!result || !result.rows || result.rows.length === 0) {
    const msg = result && result.affectedRows != null
      ? `✓ ${result.affectedRows} linha(s) afetada(s).`
      : '✓ Comando executado com sucesso.';
    container.innerHTML = `
      <div class="sql-result-inner">
        <div class="sql-result-success">${msg}</div>
        ${elapsed ? `<div class="sql-timing">⏱ ${elapsed} ms</div>` : ''}
      </div>
    `;
    return;
  }

  const { fields, rows } = result;

  // Cap display at 200 rows
  const displayRows = rows.slice(0, 200);
  const truncated = rows.length > 200;

  const headerCells = fields.map(f => `<th>${_esc(f.name)}</th>`).join('');
  const bodyRows = displayRows.map(row => {
    const cells = fields.map(f => {
      const val = row[f.name];
      const str = val === null ? '<em style="color:#666">NULL</em>' : _esc(String(val));
      return `<td title="${val === null ? 'NULL' : _esc(String(val))}">${str}</td>`;
    }).join('');
    return `<tr>${cells}</tr>`;
  }).join('');

  container.innerHTML = `
    <div style="overflow-x:auto">
      <table class="sql-result-table">
        <thead><tr>${headerCells}</tr></thead>
        <tbody>${bodyRows}</tbody>
      </table>
    </div>
    <div class="sql-timing">
      ⏱ ${elapsed} ms · ${rows.length} linha(s)${truncated ? ` · mostrando primeiras 200` : ''}
    </div>
  `;
}

function _showError(container, msg, elapsed) {
  container.innerHTML = `
    <div class="sql-result-inner">
      <div class="sql-result-error">✗ ${_esc(msg)}</div>
      ${elapsed ? `<div class="sql-timing">⏱ ${elapsed} ms</div>` : ''}
    </div>
  `;
}

function _showEmpty(container) {
  container.innerHTML = `
    <div class="sql-result-empty">
      Pressione ▶ Executar ou Ctrl+Enter para rodar o SQL.
    </div>
  `;
}

function _esc(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}
