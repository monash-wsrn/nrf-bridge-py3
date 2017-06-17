/**
 * @class WebsocketConnection
 * @desc Class to handle the connection to a webService using websockets, createConnection is meant to be used instead of the constructor
 */
export class WebsocketConnection {
    /**
     * @method createConnection
     * @desc Starts a connection to the server and creates a WebsocketConnection object
     * @param {Boolean} [consoleLogs=false] - Console logs or not on errors
     * @param {String} [address="ws://127.0.0.1:8765/"] - Address of the server to connect to
     * @param {Function} [onMessage=false] - Function to call when receiving a message
     * @param {Function} [onOpen=false] - Function to call when opening a connection
     * @param {Function} [onClose=false] - Function to call when closing a connection
     * @param {Function} [onError=false] - Function to call when an error happens
     * @returns {WebsocketConnection}
     */
    static createConnection(consoleLogs = false, onMessage = () => {},
                                                 onOpen = () => {},
                                                 onClose = () => {},
                                                 onError = () => {}, address="ws://127.0.0.1:8765/") {
        if (onOpen === (() => {}))
            onOpen = () => {
                this.send("Connection opened");
                !consoleLogs || console.log('connected');
            };

        if (onMessage === (() => {}))
            console.warn("No onMessage function provided to the connection");

        if (onClose === (() => {}))
            onClose = (evt) => {
                if (evt.code === 3001)
                    !consoleLogs || console.log('ws closed');
                else
                    !consoleLogs || console.log('ws connection error');
            };

        if (onError === (() => {}))
            onError = (evt) => {
                if (this.readyState === 1) {
                    console.log('ws normal error: ' + evt.type);
                }
            };

        let connection = new WebSocket(address);

        return new WebsocketConnection(onOpen, onMessage, onClose, onError, connection);
    }

    constructor(onOpen, onMessage, onClose, onError, connection) {
        this._websocket = connection;
        this._websocket.onopen = onOpen;
        this._websocket.onmessage = onMessage;
        this._websocket.onclose = onClose;
        this._websocket.onerror = onError;
    }

    /**
     * @method closeConnection
     * @desc Closes the websocket connection
     */
    closeConnection() {
        this._websocket.send("Closing connection");
        this._websocket.close(3001);
    }

    /**
     * @method send
     * @desc Sends data through the websocket
     * @param {*} data - data to be send
     */
    send(data) {
        this._websocket.send(data)
    }
}
