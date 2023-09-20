var location_name = "";

function appendLeadingZeroes(n){
    if(n <= 9){
        return "0" + n;
    }
    return n
}

// startup socket connection
socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
// console.log(socket);

// Function that shows all the logs
function append_to_log(text) {
    var today = new Date();
    var time = appendLeadingZeroes(today.getHours()) + ":" + appendLeadingZeroes(today.getMinutes()) + ":" + appendLeadingZeroes(today.getSeconds());
    $('#log').prepend('<br>' + $('<div/>').text(time + " - " + text).html());
};

// Message when client is connected
socket.on('connect', function() {
    // append_to_log('connected! ' + location_name);
    console.log('connected!');
});

// Message when there is a connection error
socket.on("connect_error", (err) => {
    console.log(`connect_error due to ${err.message}`);
});