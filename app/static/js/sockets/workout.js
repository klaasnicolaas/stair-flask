// Send data to server
system_control = function(event) {
    socket.emit('system_control', {data: event});
};