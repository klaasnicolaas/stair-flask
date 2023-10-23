var timerInterval
var isOefeningGestart = false
$('#alert-container').hide()

// Send data to server
system_control = function (event) {
  let workout_id = $('#workout_id').data('name')
  let time = calculateTotalSeconds($('#input_time').val())
  let end_sensor = $('input[name="list-sensor-end"]:checked').val()
  let led_toggle = $('#led_toggle').is(':checked')
  let brightness = $('#brightness_value').val()
  let color = $('#color-picker').val()

  // Update the workout status
  if (event == 'start') {
    if (workout_id == 2) {
      resetTimer()
      startTimer()
    }
    isOefeningGestart = true
    updateOefeningStatus()
  } else if (event == 'stop' || event == 'finished') {
    if (workout_id == 2) {
      resetTimer()
    }
    isOefeningGestart = false
    updateOefeningStatus()
  }

  // Send data to server based on workout_id
  if (workout_id == 2) {
    console.log(event, workout_id, time, end_sensor, led_toggle, brightness, color)
    socket.emit('system_control', { mode: event, workout_id: workout_id, time: time, end_sensor: end_sensor, led_toggle: led_toggle, brightness: brightness, color: color })
  } else {
    console.log(event, workout_id)
    socket.emit('system_control', { mode: event, workout_id: workout_id })
  }
}

socket.on('counter', function (data) {
  $('#counter_stairs').text(data)
})

// Function to update the alert message
function updateOefeningStatus() {
  var alertContainer = $('#alert-container')
  var alertMessage = alertContainer.find('div')

  if (isOefeningGestart) {
    alertContainer.removeClass('text-red-800 border-red-300 bg-red-50 dark:bg-gray-800 dark:text-red-400 dark:border-red-800')
    alertContainer.addClass('text-green-800 border-green-300 bg-green-50 dark:bg-gray-800 dark:text-green-400 dark:border-green-800')
    alertMessage.html("<span class='font-medium'>Let op!</span> De oefening is gestart!")
    alertContainer.show() // Toon de alert
  } else {
    alertContainer.removeClass('text-green-800 border-green-300 bg-green-50 dark:bg-gray-800 dark:text-green-400 dark:border-green-800')
    alertContainer.addClass('text-red-800 border-red-300 bg-red-50 dark:bg-gray-800 dark:text-red-400 dark:border-red-800')
    alertMessage.html("<span class='font-medium'>Let op!</span> De oefening is gestopt.")
    alertContainer.show() // Toon de alert
    setTimeout(function () {
      alertContainer.hide() // Verberg de alert na 10 seconden
    }, 5000)
  }
}

// Update the workout countdown timer
$('#input_time').on('input', function () {
  updateTimerDisplay()
})

// Update the workout show timer
function updateTimerDisplay() {
  var inputTime = $('#input_time').val()
  var timerElement = $('#show_timer')

  var timeParts = inputTime.split(':')
  var hours = parseInt(timeParts[0]) || 0 // Zorg ervoor dat hours altijd een getal is (standaard naar 0)
  var minutes = parseInt(timeParts[1]) || 0 // Zorg ervoor dat minutes altijd een getal is (standaard naar 0)
  var seconds = parseInt(timeParts[2]) || 0 // Zorg ervoor dat seconds altijd een getal is (standaard naar 0)

  var displayHours = hours.toString().padStart(2, '0')
  var displayMinutes = minutes.toString().padStart(2, '0')
  var displaySeconds = seconds.toString().padStart(2, '0')

  timerElement.text(displayHours + ':' + displayMinutes + ':' + displaySeconds)
}

// Reset de workout-timer
function resetTimer() {
  clearInterval(timerInterval) // Stop de timer interval
  timerInterval = null

  // Update de timerweergave om de oorspronkelijke tijd te tonen
  updateTimerDisplay()
}

var timerInterval = null // Variabele om de timerinterval bij te houden

// Calculate the total seconds based on the string input time
function calculateTotalSeconds(timeString) {
  if (!timeString) {
    return null
  }

  let timeParts = timeString.split(':')
  let hours = parseInt(timeParts[0]) || 0
  let minutes = parseInt(timeParts[1]) || 0
  let totalSeconds = hours * 3600 + minutes * 60

  return totalSeconds
}

function startTimer() {
  // Voorkom dat de timer opnieuw wordt gestart als deze al loopt
  if (timerInterval) {
    return
  }

  var totalSeconds = calculateTotalSeconds($('#input_time').val())

  function updateTimer() {
    var displayHours = Math.floor(totalSeconds / 3600)
    var remainingSeconds = totalSeconds % 3600
    var displayMinutes = Math.floor(remainingSeconds / 60)
    var displaySeconds = remainingSeconds % 60

    $('#show_timer').text(displayHours.toString().padStart(2, '0') + ':' + displayMinutes.toString().padStart(2, '0') + ':' + displaySeconds.toString().padStart(2, '0'))

    if (totalSeconds <= 0) {
      clearInterval(timerInterval)
      timerInterval = null // Verwijder de interval
      system_control('finished') // Stop de oefening
    } else {
      totalSeconds--
    }
  }

  // Start de timer en update de timerweergave
  updateTimer()
  timerInterval = setInterval(updateTimer, 1000)
}

$(document).ready(function () {
  // Get references to the slider and the element to display the value
  const brightnessSlider = $('#brightness_value')
  const brightnessNumber = $('#brightness_number')

  // Add an event listener to the slider
  brightnessSlider.on('input', function () {
    // Update the value displayed based on the slider value
    brightnessNumber.text($(this).val()) // Use $(this).val() to get the slider value
  })
})

// Change the order of the cards based on the orientation
$(screen.orientation).on('change', function () {
  console.log('Orientation changed')
  // Controleer of het scherm in portrait mode is
  if (screen.orientation.type === 'portrait-primary' || screen.orientation.type === 'portrait-secondary') {
    // Verander de volgorde van de kaarten voor portrait mode
    $('#timeCard').css('order', 2)
    $('#settingsCard').css('order', 3)
    $('#controlCard').css('order', 1)
  } else {
    // Reset de volgorde voor landscape mode
    $('#timeCard').css('order', '')
    $('#settingsCard').css('order', '')
    $('#controlCard').css('order', '')
  }
})
