/**
 * Created by tanguy on 20/03/17.
 */

export class WebsocketConnection {
    static createConnection(consoleLogs = false, onMessage = false, onOpen = false, onClose = false, onError = false) {
        if (!onOpen)
            onOpen = function () {
                this.send("Connection opened");
                !consoleLogs || console.log('connected');
            };
        if (!onMessage) {
            onMessage = function () {
            }
            console.warn("No onMessage function provided to the connection")
        }
        if (!onClose) {
            onClose = function (evt) {
                if (evt.code == 3001)
                    !consoleLogs || console.log('ws closed');
                else
                    !consoleLogs || console.log('ws connection error');
            };
        }
        if (!onError) {
            onError = function (evt) {
                if (this.readyState == 1) {
                    console.log('ws normal error: ' + evt.type);
                }
            };
        }

        let connection = new WebSocket("ws://127.0.0.1:8765/");

        return new WebsocketConnection(onOpen, onMessage, onClose, onError, connection);
    }

    constructor(onOpen, onMessage, onClose, onError, connection) {
        this._websocket = connection;
        this._websocket.onopen = onOpen;
        this._websocket.onmessage = onMessage;
        this._websocket.onclose = onClose;
        this._websocket.onerror = onError;
    }

    closeConnection() {
        this._websocket.send("Closing connection");
        this._websocket.close(3001);
    }

    send(data) {
        this._websocket.send(data)
    }
}
