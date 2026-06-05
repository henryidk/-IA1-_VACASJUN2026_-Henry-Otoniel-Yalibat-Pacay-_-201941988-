const API = 'http://localhost:8000/api';



document.addEventListener('DOMContentLoaded', () => {
  inicializarTabs();
  cargarCiudades();

  document.getElementById('btn-buscar').addEventListener('click', buscarRutas);
  document.getElementById('btn-limpiar').addEventListener('click', limpiarBusqueda);
});

// TABS


function inicializarTabs() {
  document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', () => {
      document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach(c => {
        c.classList.remove('active');
        c.classList.add('hidden');
      });
      tab.classList.add('active');
      const target = document.getElementById(`tab-${tab.dataset.tab}`);
      target.classList.remove('hidden');
      target.classList.add('active');
    });
  });
}

// CARGAR CIUDADES EN DROPDOWNS


async function cargarCiudades() {
  try {
    const res = await fetch(`${API}/ciudades`);
    const data = await res.json();
    const ciudades = data.ciudades.map(c => formatearNombre(c));

    ['origen', 'destino'].forEach(id => {
      const select = document.getElementById(id);
      select.innerHTML = `<option value="">-- Selecciona ${id} --</option>`;
      data.ciudades.forEach((ciudad, i) => {
        const opt = document.createElement('option');
        opt.value = ciudad;
        opt.textContent = ciudades[i];
        select.appendChild(opt);
      });
    });

    // También poblar el select de conexiones en gestión de ciudades
    poblarSelectConexiones(data.ciudades);
  } catch {
    mostrarAlerta('alerta', 'No se pudo conectar con el servidor.', 'error');
  }
}

function poblarSelectConexiones(ciudades) {
  document.querySelectorAll('.conexion-destino').forEach(select => {
    const valorActual = select.value;
    select.innerHTML = '<option value="">-- Ciudad destino --</option>';
    ciudades.forEach(c => {
      const opt = document.createElement('option');
      opt.value = c;
      opt.textContent = formatearNombre(c);
      select.appendChild(opt);
    });
    if (valorActual) select.value = valorActual;
  });
}


// BUSCAR RUTAS

async function buscarRutas() {
  const origen = document.getElementById('origen').value;
  const destino = document.getElementById('destino').value;

  ocultarAlerta('alerta');
  document.getElementById('resultados').classList.add('hidden');

  if (!origen || !destino) {
    mostrarAlerta('alerta', 'Por favor selecciona una ciudad de origen y una de destino.', 'error');
    return;
  }

  try {
    const [resRutas, resCorta] = await Promise.all([
      fetch(`${API}/rutas`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ origen, destino })
      }),
      fetch(`${API}/ruta-corta`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ origen, destino })
      })
    ]);

    if (!resRutas.ok) {
      const err = await resRutas.json();
      mostrarAlerta('alerta', err.detail, 'error');
      return;
    }

    const dataRutas = await resRutas.json();
    const dataCorta = await resCorta.json();

    renderizarRutaCorta(dataCorta.ruta_mas_corta);
    renderizarEstadisticas(dataRutas.estadisticas);
    renderizarListaRutas(dataRutas.rutas);

    document.getElementById('resultados').classList.remove('hidden');
  } catch {
    mostrarAlerta('alerta', 'Error al conectar con el servidor.', 'error');
  }
}

// RENDERIZADO DE RESULTADOS

function renderizarRutaCorta(ruta) {
  const caminoEl = document.getElementById('ruta-corta-camino');
  const distEl = document.getElementById('ruta-corta-distancia');

  caminoEl.innerHTML = ruta.camino.map((ciudad, i) => {
    const chip = `<span class="ciudad-chip">${formatearNombre(ciudad)}</span>`;
    const flecha = i < ruta.camino.length - 1 ? '<span class="flecha">→</span>' : '';
    return chip + flecha;
  }).join('');

  distEl.textContent = `${ruta.distancia} km`;
}

function renderizarEstadisticas(stats) {
  document.getElementById('stat-total').textContent = stats.total_rutas;
  document.getElementById('stat-min').textContent = `${stats.distancia_minima} km`;
  document.getElementById('stat-max').textContent = `${stats.distancia_maxima} km`;
  document.getElementById('stat-prom').textContent = `${stats.distancia_promedio} km`;
}

function renderizarListaRutas(rutas) {
  const lista = document.getElementById('lista-rutas');
  lista.innerHTML = rutas.map((ruta, i) => `
    <div class="ruta-item">
      <div class="ruta-numero ${i === 0 ? 'primero' : ''}">${i + 1}</div>
      <div class="ruta-detalle">
        <div class="ruta-ciudades">${ruta.camino.map(formatearNombre).join(' → ')}</div>
      </div>
      <div class="ruta-distancia">${ruta.distancia} km</div>
    </div>
  `).join('');
}

// =====================================================================
// LIMPIAR BÚSQUEDA
// =====================================================================

function limpiarBusqueda() {
  document.getElementById('origen').value = '';
  document.getElementById('destino').value = '';
  document.getElementById('resultados').classList.add('hidden');
  ocultarAlerta('alerta');
}

// =====================================================================
// UTILIDADES
// =====================================================================

function formatearNombre(nombre) {
  return nombre.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
}

function mostrarAlerta(id, mensaje, tipo) {
  const el = document.getElementById(id);
  el.textContent = mensaje;
  el.className = `alerta alerta-${tipo}`;
}

function ocultarAlerta(id) {
  const el = document.getElementById(id);
  el.className = 'alerta hidden';
}
