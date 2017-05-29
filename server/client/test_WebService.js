let _websocket;

function wsConnect() {
    if (_websocket) {
        _websocket.close(3001);
    }
    _websocket = new WebSocket("ws://127.0.0.1:8765/");
    _websocket.onopen = function () {
        _websocket.send("Connection opened");
        console.log('connected');
    };
    _websocket.onmessage = function (msg) {
        document.getElementById("pointsView").innerText = JSON.stringify(msg.data);

    };

    _websocket.onclose = function (evt) {
        if (evt.code == 3001) {
            console.log('ws closed');
            _websocket = null;
        } else {
            _websocket = null;
            document.getElementById("pointsView").innerHTML = "<h1>Connection error</h1>";
            console.log('ws connection error');
        }
    };

    _websocket.onerror = function (evt) {
        if (_websocket.readyState == 1) {
            console.log('ws normal error: ' + evt.type);
        }
    };

}


function sendPing() {
    if (_websocket)
        _websocket.send("ping")
}

function closeConnection() {
    if (_websocket) {
        _websocket.send("Closing connection");
        _websocket.close(3001);
    }
}
window.addEventListener("beforeunload", function (event) {
    event.preventDefault();
    closeConnection();
});

