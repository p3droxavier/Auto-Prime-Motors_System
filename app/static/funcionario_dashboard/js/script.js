/* ANIMAÇÃO  DE ESCOLHER OPÇÃO SIDE BAR */
const allSideMenu = document.querySelectorAll('#sidebar .side-menu.top li a');

allSideMenu.forEach(item => {
  const li = item.parentElement;

  item.addEventListener('click', function () {
    allSideMenu.forEach(i => {
      i.parentElement.classList.remove('active')
    })

    li.classList.add('active');
  })
})
/* ==================================== */



/* ANIMAÇÃO PARA DIMINUIR O SIDEBAR */
const menuBar = document.querySelector('#content nav .bxr.bx-menu-wider') // SE DER ERRO PODE SER AQUI
const sidebar = document.getElementById('sidebar')

//Atribui o 'hide' dinamicamente  
menuBar.addEventListener('click', function () {
  sidebar.classList.toggle('hide')
})
/* ================================ */





/* AJUSTANDO O TAMANHO DOS COMPONENTES DA NAVBAR */
const searchButton = document.querySelector('#content nav form .form-input button')
const searchButtonIcon = document.querySelector('#content nav form .form-input button .bxr')
const searchForm = document.querySelector('#content nav form')

searchButton.addEventListener('click', function (e) {
  if (window.innerWidth < 576) {
    e.preventDefault();
    searchForm.classList.toggle('show')
    if (searchForm.classList.contains('show')) {
      searchButtonIcon.classList.replace('bx-search', 'bx-x')
    } else {
      searchButtonIcon.classList.replace('bx-x', 'bx-search')
    }
  }

})


if (window.innerWidth < 830) {
  sidebar.classList.add('hide')
} else if (window.innerWidth < 576) {
  searchButtonIcon.classList.replace('bx-x', 'bx-search')
  searchForm.classList.toggle('show')
}


window.addEventListener('resize', function () {
  if (this.innerWidth < 576) {
    searchButtonIcon.classList.replace('bx-x', 'bx-search')
    searchForm.classList.toggle('show')
  }
})
/* ============================================= */
