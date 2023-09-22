socket.on('sensors_status_all', function(msg) {
    // Update the status of a specific sensor on index page
    $('#js--sensor-'+ msg.client_id +'_status').text(msg.status);
    if (msg.status == 'offline' || msg.status == 'error') {
        $('#js--sensor-'+ msg.client_id +'_state').text('🔴');
    } else if (msg.status == 'online') {
        $('#js--sensor-'+ msg.client_id +'_state').text('🟣');
    } else {
        $('#js--sensor-'+ msg.client_id +'_state').text('🟢');
    }
});