var sensorID = $('#sensor_id').data('name').slice(7);
var eventName = 'sensor_status_' + sensorID;

socket.on(eventName, function (msg) {
  append_to_status_log(msg)
  $('#js--sensor_status').text(msg.status);
  $('#js--sensor_trigger_distance').text(msg.distance);
  $('.sensor-threshold').text(msg.threshold);
  $('#js--sensor_max_distance').text(msg.max_distance);
  $('#js--threshold_progress_bar').css('width', calculatePercentage(msg.threshold, msg.max_distance) + '%');
})

// Function to calculate the percentage of the threshold
function calculatePercentage(distance, maxDistance) {
  return (distance / maxDistance) * 100;
}

function capitalizeFirstLetter(string) {
  return string.charAt(0).toUpperCase() + string.slice(1);
}

// Function that shows all the logs
function append_to_status_log(jsonData) {
  var today = new Date()
  var time = appendLeadingZeroes(today.getHours()) + ':' + appendLeadingZeroes(today.getMinutes()) + ':' + appendLeadingZeroes(today.getSeconds())

  const status = jsonData.status
  const threshold = jsonData.threshold
  const maxDistance = jsonData.max_distance

  let listItem;

  if (status == 'trigger') {
    const distance = jsonData.distance
    listItem = $('<li>').html(time + ' - <strong>' + capitalizeFirstLetter(status) + '</strong> - Distance: ' + distance + ' mm')
  } else {
    listItem = $('<li>').html(time + ' - <strong>' + capitalizeFirstLetter(status) + '</strong> - Thres: ' + threshold + ' mm - MaxDist: ' + maxDistance + ' mm');
  }
  $('#log-list').prepend(listItem);
  limitLogItems();
}
