// Show the SA for restarting a single sensor
restart_sensor = function (event) {
  Swal.fire({
    title: 'Weet je het zeker?',
    text: 'Wanneer je deze actie uitvoert wordt de sensor opnieuw opgestart.',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#EF7D00',
    cancelButtonText: "Annuleren",
    confirmButtonText: 'Herstart',
  }).then((result) => {
    if (result.isConfirmed) {
      socket.emit('restart_sensors', event)
    }
  })
}

// Show the SA for restarting all sensors
restart_all_sensors = function(event) {
    Swal.fire({
      title: 'Weet je het zeker?',
      text: 'Wanneer je deze actie uitvoert worden alle sensoren opnieuw opgestart.',
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#EF7D00',
      cancelButtonText: "Annuleren",
      confirmButtonText: 'Herstart',
    }).then((result) => {
      if (result.isConfirmed) {
        socket.emit('restart_sensors', event);
      }
    })
  }
