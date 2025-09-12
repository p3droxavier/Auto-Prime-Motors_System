/* COMPONENTES DASHBOARD ADMINISTRADOR */
function showTabAdmin(tab) {
  document.getElementById('todos_os_funcionarios_tab').style.display = tab === 'todos_os_funcionarios' ? 'block' : 'none';
  document.getElementById('todos_os_setores_tab').style.display = tab === 'todos_os_setores' ? 'block' : 'none';
  document.getElementById('postar_nova_tarefa_tab').style.display = tab === 'postar_nova_tarefa' ? 'block' : 'none';
}