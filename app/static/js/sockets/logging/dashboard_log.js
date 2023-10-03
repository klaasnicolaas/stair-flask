socket.on("sensors_status_all", function (msg) {
  append_to_status_log(msg)
})

function append_to_status_log(jsonData) {
  var today = new Date()
  var time = appendLeadingZeroes(today.getHours()) + ':' + appendLeadingZeroes(today.getMinutes()) + ':' + appendLeadingZeroes(today.getSeconds())

  const status = jsonData.status
  const sensorID = jsonData.client_id
  const threshold = jsonData.threshold
  const maxDistance = jsonData.max_distance

  let listItem;

  if (status == 'trigger') {
    const distance = jsonData.distance
    listItem = $('<li>').html(time + ' - Sensor <strong>' + sensorID + '</strong> is: ' + status + ' - D: ' + distance + ' mm')
  } else {
    listItem = $('<li>').html(time + ' - Sensor <strong>' + sensorID + '</strong> is: ' + status + ' - T: ' + threshold + ' mm - Md: ' + maxDistance + ' mm');
  }

  $('#log-list').prepend(listItem)
  limitLogItems(8)
}
