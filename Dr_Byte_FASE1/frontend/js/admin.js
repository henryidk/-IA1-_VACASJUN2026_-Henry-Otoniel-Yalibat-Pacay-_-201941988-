const API = '/api/admin';

// ------------------------------------------------------------------ INICIO
document.addEventListener('DOMContentLoaded', cargarTodo);

async function cargarTodo() {
  await Promise.all([cargarSintomas(), cargarFallas()]);
}

// ------------------------------------------------------------ AUTO ID
function generarId(texto) {
  return texto.toLowerCase()
    .normalize('NFD').replace(/[̀-ͯ]/g, '')
    .replace(/[^a-z0-9\s]/g, '')
    .trim()
    .replace(/\s+/g, '_')
    .substring(0, 40);
}

function previsualizarIdSintoma(texto) {
  document.getElementById('s-id-preview').textContent = generarId(texto) || '—';
}

function previsualizarIdFalla(texto) {
  document.getElementById('f-id-preview').textContent = generarId(texto) || '—';
}

// ----------------------------------------------------------------- FEEDBACK
function mostrarAlerta(mensaje, tipo = 'success') {
  const el = document.getElementById('alerta-global');
  el.className = `alert alert-${tipo}`;
  el.textContent = mensaje;
  el.classList.remove('d-none');
  setTimeout(() => el.classList.add('d-none'), 3500);
}

// ------------------------------------------------------------------ FETCH
async function apiFetch(url, opciones = {}) {
  const res = await fetch(url, {
    headers: { 'Content-Type': 'application/json' },
    ...opciones,
  });
  return { ok: res.ok, data: await res.json() };
}

// ================================================================ SÍNTOMAS

async function cargarSintomas() {
  const [{ data: sintomas }, { data: reglas }, { data: fallas }] = await Promise.all([
    apiFetch(`${API}/sintomas`),
    apiFetch(`${API}/reglas`),
    apiFetch(`${API}/fallas`),
  ]);

  // Actualizar dropdown de fallas en el formulario de síntomas
  const sel = document.getElementById('s-falla');
  const valorActual = sel.value;
  sel.innerHTML = `<option value="">— Selecciona una falla —</option>` +
    fallas.map(f => `<option value="${f.id}">${f.descripcion}</option>`).join('');
  sel.value = valorActual;

  // Construir mapa sintoma → falla
  const mapa = {};
  reglas.forEach(r => {
    if (!mapa[r.sintoma]) mapa[r.sintoma] = [];
    mapa[r.sintoma].push(r.falla);
  });

  const lista = document.getElementById('lista-sintomas');
  if (!sintomas.length) {
    lista.innerHTML = '<p class="text-muted">No hay síntomas registrados.</p>';
    return;
  }

  lista.innerHTML = `
    <table class="table table-sm table-hover align-middle">
      <thead class="table-light">
        <tr>
          <th>Síntoma</th>
          <th>Indica</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        ${sintomas.map(s => {
          const fallas_asociadas = mapa[s.id] || [];
          const badge = fallas_asociadas.length
            ? fallas_asociadas.map(f => `<span class="me-1" style="display:inline-block;background:#89D7B7;color:#1A312C;border-radius:20px;font-size:0.78rem;padding:2px 10px;font-weight:500;">${f}</span>`).join('')
            : '<span class="text-muted small">Sin regla</span>';
          return `
            <tr>
              <td style="border-right: 1px solid #d4e6df;">${s.descripcion}</td>
              <td>${badge}</td>
              <td class="text-end">
                <button class="btn btn-sm btn-outline-danger" onclick="eliminarSintoma('${s.id}')">
                  <i class="bi bi-trash"></i>
                </button>
              </td>
            </tr>`;
        }).join('')}
      </tbody>
    </table>`;
}

async function agregarSintoma() {
  const desc  = document.getElementById('s-desc').value.trim();
  const falla = document.getElementById('s-falla').value;
  const id    = generarId(desc);

  if (!desc) { mostrarAlerta('Escribe la descripción del síntoma.', 'warning'); return; }
  if (!falla) { mostrarAlerta('Selecciona la falla que indica este síntoma.', 'warning'); return; }

  // Crear síntoma
  const { ok, data } = await apiFetch(`${API}/sintomas`, {
    method: 'POST', body: JSON.stringify({ id, descripcion: desc })
  });
  if (!ok) { mostrarAlerta(data.error, 'danger'); return; }

  // Crear la regla automáticamente
  await apiFetch(`${API}/reglas`, {
    method: 'POST', body: JSON.stringify({ sintoma: id, falla })
  });

  mostrarAlerta(`Síntoma "${desc}" agregado correctamente.`);
  document.getElementById('s-desc').value = '';
  document.getElementById('s-id-preview').textContent = '—';
  document.getElementById('s-falla').value = '';
  await cargarSintomas();
}

async function eliminarSintoma(id) {
  if (!confirm(`¿Eliminar este síntoma y sus reglas asociadas?`)) return;
  const { ok, data } = await apiFetch(`${API}/sintomas/${id}`, { method: 'DELETE' });
  mostrarAlerta(data.mensaje || data.error, ok ? 'success' : 'danger');
  if (ok) await cargarSintomas();
}

// ================================================================== FALLAS

async function cargarFallas() {
  const [{ data: fallas }, { data: todasRec }] = await Promise.all([
    apiFetch(`${API}/fallas`),
    apiFetch(`${API}/recomendaciones`),
  ]);

  const lista = document.getElementById('lista-fallas');
  if (!fallas.length) {
    lista.innerHTML = '<p class="text-muted">No hay fallas registradas.</p>';
    return;
  }

  lista.innerHTML = `<div class="accordion" id="acordeon-fallas">` +
    fallas.map((f, i) => {
      const recs = todasRec.filter(r => r.falla === f.id);
      const listaRecs = recs.length
        ? recs.map(r => `
            <div class="d-flex justify-content-between align-items-start py-1 border-bottom">
              <small class="text-secondary">${r.texto}</small>
              <button class="btn btn-sm text-danger border-0 p-0 ms-2 flex-shrink-0"
                onclick="eliminarRecomendacion('${f.id}', \`${r.texto.replace(/`/g, '\\`')}\`)">
                <i class="bi bi-x-lg"></i>
              </button>
            </div>`).join('')
        : '<p class="text-muted small mb-2">Sin recomendaciones aún.</p>';

      return `
        <div class="accordion-item">
          <h2 class="accordion-header">
            <button class="accordion-button collapsed d-flex justify-content-between" type="button"
              data-bs-toggle="collapse" data-bs-target="#falla-${i}">
              <span>
                ${f.descripcion}
                <span class="ms-2" style="display:inline-block;background:#1A312C;color:#89D7B7;border-radius:20px;font-size:0.78rem;font-weight:600;padding:2px 9px;">${recs.length}</span>
              </span>
            </button>
          </h2>
          <div id="falla-${i}" class="accordion-collapse collapse" data-bs-parent="#acordeon-fallas">
            <div class="accordion-body pt-2">
              <div class="mb-3">${listaRecs}</div>
              <div class="d-flex gap-2 mb-2">
                <input type="text" id="rec-${f.id}" class="form-control form-control-sm"
                  placeholder="Nueva recomendación..." />
                <button class="btn btn-sm btn-outline-primary text-nowrap"
                  onclick="agregarRecomendacion('${f.id}')">
                  <i class="bi bi-plus-lg"></i> Agregar
                </button>
              </div>
              <button class="btn btn-sm btn-outline-danger w-100"
                onclick="eliminarFalla('${f.id}')">
                <i class="bi bi-trash me-1"></i>Eliminar esta falla
              </button>
            </div>
          </div>
        </div>`;
    }).join('') + `</div>`;
}

async function agregarFalla() {
  const desc = document.getElementById('f-desc').value.trim();
  const id   = generarId(desc);

  if (!desc) { mostrarAlerta('Escribe la descripción de la falla.', 'warning'); return; }

  const { ok, data } = await apiFetch(`${API}/fallas`, {
    method: 'POST', body: JSON.stringify({ id, descripcion: desc })
  });

  mostrarAlerta(data.mensaje || data.error, ok ? 'success' : 'danger');
  if (ok) {
    document.getElementById('f-desc').value = '';
    document.getElementById('f-id-preview').textContent = '—';
    await Promise.all([cargarFallas(), cargarSintomas()]);
  }
}

async function eliminarFalla(id) {
  if (!confirm(`¿Eliminar esta falla, sus reglas y recomendaciones?`)) return;
  const { ok, data } = await apiFetch(`${API}/fallas/${id}`, { method: 'DELETE' });
  mostrarAlerta(data.mensaje || data.error, ok ? 'success' : 'danger');
  if (ok) await Promise.all([cargarFallas(), cargarSintomas()]);
}

async function agregarRecomendacion(idFalla) {
  const input = document.getElementById(`rec-${idFalla}`);
  const texto = input.value.trim();
  if (!texto) { mostrarAlerta('Escribe el texto de la recomendación.', 'warning'); return; }

  const { ok, data } = await apiFetch(`${API}/recomendaciones`, {
    method: 'POST', body: JSON.stringify({ falla: idFalla, texto })
  });

  mostrarAlerta(data.mensaje || data.error, ok ? 'success' : 'danger');
  if (ok) { input.value = ''; await cargarFallas(); }
}

async function eliminarRecomendacion(idFalla, texto) {
  const { ok, data } = await apiFetch(`${API}/recomendaciones`, {
    method: 'DELETE', body: JSON.stringify({ falla: idFalla, texto })
  });
  mostrarAlerta(data.mensaje || data.error, ok ? 'success' : 'danger');
  if (ok) await cargarFallas();
}
