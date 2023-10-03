// Message when client is connected
socket.on('connect', function () {
  append_to_log('connected!')
})

function appendLeadingZeroes(n) {
  if (n <= 9) {
    return '0' + n
  }
  return n
}

// Function that shows all the logs
function append_to_log(data) {
  var today = new Date()
  var time = appendLeadingZeroes(today.getHours()) + ':' + appendLeadingZeroes(today.getMinutes()) + ':' + appendLeadingZeroes(today.getSeconds())

  const listItem = $('<li>').text(time + ' - ' + data)
  $('#log-list').prepend(listItem)
  limitLogItems()
}

function limitLogItems(number) {
  let maxItems = number || 15
  const logList = $('#log-list')

  while (logList.children().length > maxItems) {
    logList.children().last().remove()
  }
}
