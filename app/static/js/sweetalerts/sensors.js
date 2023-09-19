const deleteButton = document.querySelector('#delete-all')

deleteButton.addEventListener('click', (event) => {
  event.preventDefault()
  Swal.fire({
    title: 'Weet je het zeker?',
    text: 'Wanneer je deze actie uitvoert worden alle sensoren verwijderd.',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonText: 'Delete',
  }).then((result) => {
    if (result.isConfirmed) {
      event.target.closest('form').submit()
    }
  })
})
