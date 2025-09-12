/* COMPONENTES DASHBOARD FUNCIONARIOS */

function showTab(tab) {
  document.getElementById('meus_dados_tab').style.display = tab === 'meus_dados' ? 'block' : 'none';
  document.getElementById('tarefas_tab').style.display = tab === 'tarefas' ? 'block' : 'none';
}