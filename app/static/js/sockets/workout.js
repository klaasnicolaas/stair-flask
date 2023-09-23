// Send data to server
system_control = function(event) {
    let workout_id = $('#workout_id').data('name');
    socket.emit('system_control', {mode: event, workout_id: workout_id});
};