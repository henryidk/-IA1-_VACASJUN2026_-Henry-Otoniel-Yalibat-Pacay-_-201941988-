const API = 'http://localhost:8000/api';

document.addEventListener('DOMContentLoaded', () => {
  // Lógica de tabs y funcionalidad se agrega en partes 4.2 y 4.3
  document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', () => {
      document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach(c => c.classList.add('hidden'));
      document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
      tab.classList.add('active');
      const target = document.getElementById(`tab-${tab.dataset.tab}`);
      target.classList.remove('hidden');
      target.classList.add('active');
    });
  });
});
