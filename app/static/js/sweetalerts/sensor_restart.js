restart_sensor = function (event) {
  Swal.fire({
    title: 'Weet je het zeker?',
    text: 'Wanneer je deze actie uitvoert wordt de sensor opnieuw opgestart.',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonText: 'Restart',
  }).then((result) => {
    if (result.isConfirmed) {
      socket.emit('restart_sensors', event)
    }
  })
}

restart_all_sensors = function(event) {
    Swal.fire({
      title: 'Weet je het zeker?',
      text: 'Wanneer je deze actie uitvoert worden alle sensoren opnieuw opgestart.',
      icon: 'warning',
      showCancelButton: true,
      confirmButtonText: 'Restart',
    }).then((result) => {
      if (result.isConfirmed) {
        socket.emit('restart_sensors', event);
      }
    })
  }
