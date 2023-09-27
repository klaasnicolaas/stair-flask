function appendLeadingZeroes(n){
    if(n <= 9){
        return "0" + n;
    }
    return n
}

// Function that shows all the logs
function append_to_log(text) {
    var today = new Date();
    var time = appendLeadingZeroes(today.getHours()) + ":" + appendLeadingZeroes(today.getMinutes()) + ":" + appendLeadingZeroes(today.getSeconds());

    const logList = document.getElementById('log-list');
    const listItem = document.createElement('li');
    listItem.textContent = time + " - " + text;
    logList.appendChild(listItem);
};

// Message when client is connected
socket.on('connect', function() {
    append_to_log('connected!');
    // console.log('connected!');
});
