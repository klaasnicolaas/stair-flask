// Show the SA for deleting all sensors
$('#delete-all-sensors').click(function(event) {
  event.preventDefault();

  Swal.fire({
    title: 'Weet je het zeker?',
    text: 'Wanneer je deze actie uitvoert worden alle sensoren verwijderd.',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#EF7D00',
    cancelButtonText: "Annuleren",
    confirmButtonText: 'Verwijder',
  }).then((result) => {
    if (result.isConfirmed) {
      $(event.target).closest('form').submit();
    }
  });
});

// Show the SA for deleting a single sensor
$('#delete-single-sensor').click(function(event) {
  event.preventDefault();

  Swal.fire({
    title: 'Weet je het zeker?',
    text: 'Wanneer je deze actie uitvoert wordt deze sensor verwijderd.',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#EF7D00',
    cancelButtonText: "Annuleren",
    confirmButtonText: 'Verwijder',
  }).then((result) => {
    if (result.isConfirmed) {
      $(event.target).closest('form').submit();
    }
  });
});
