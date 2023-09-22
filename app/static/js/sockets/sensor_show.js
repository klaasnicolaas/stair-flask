var sensorID = $('#sensor_id').data('name').slice(7);
var eventName = 'sensor_status_' + sensorID;

socket.on(eventName, function (msg) {
  append_to_status_log(msg)
  $('#js--sensor_status').text(msg.status);
  limitLogItems();
})

// Function that shows all the logs
function append_to_status_log(jsonData) {
  var today = new Date()
  var time = appendLeadingZeroes(today.getHours()) + ':' + appendLeadingZeroes(today.getMinutes()) + ':' + appendLeadingZeroes(today.getSeconds())

  const status = jsonData.status
  const threshold = jsonData.threshold
  const maxDistance = jsonData.max_distance

  const listItem = $('<li>').text(time + ' - Sensor is: ' + status + ' - T: ' + threshold + ' mm - Md: ' + maxDistance + ' mm');
  $('#log-list').prepend(listItem);
  limitLogItems();
}

function limitLogItems() {
  const maxItems = 15;
  const logList = $('#log-list');

  while (logList.children().length > maxItems) {
    logList.children().last().remove();
  }
}
