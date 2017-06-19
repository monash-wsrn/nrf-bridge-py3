//Radius of the gradient
export const GRADIENT_RADIUS = 100;

//Triangle constants
export const ROBOT_TRIANGLE_HEIGHT = Math.sqrt((16 * 16) - 64);
export const x1 = -8, y1 = 0, x2 = 8, y2 = 0, x3 = 0, y3 = -ROBOT_TRIANGLE_HEIGHT;

//Robot constants (Used only in default)
export const ROBOT_WIDTH = 45;
export const ROBOT_COLOR = "#FFFFFF";
export const ROBOT_TEXT_SIZE = 20;
export const ROBOT_TRIANGLE_COLOR = "#FF0000";

//Constants dealing with timeouts
//Timeout a tracked position is recorded out of the positions received
//For example 10 means that every 10 position received is added to tracked positions
export const TRACKING_TIMEOUT = 10;
//Timeout the after move actions are triggered out of the positions received
export const AFTER_MOVE_TIMEOUT = 10;
//Number of colors a tracked positions may take before fading
export const LIFESPAN = 250;
//Timeout between two fades of a tracked position, the smaller it is the quickly the tracked positions fade
export const FADING_TIMEOUT = 100;

//Websocket server default address
export const WEBSOCKET_SERVER_ADDRESS = "ws://127.0.0.1:8765/";
