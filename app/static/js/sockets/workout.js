system_active = function(event) {
    socket.emit('active', {data: event});
};