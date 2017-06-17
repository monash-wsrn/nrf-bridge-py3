import {RobotTrackedPositionManager} from "./trackedPosition"
import {Gradient} from "./gradient"

//Triangle constants
let ROBOT_TRIANGLE_HEIGHT = Math.sqrt((16 * 16) - 64);
let x1 = -8, y1 = 0, x2 = 8, y2 = 0, x3 = 0, y3 = -ROBOT_TRIANGLE_HEIGHT;

//Options Constants
let TRACKING_TIMEOUT = 10;

/**
 * @class Robot
 * @desc Class to represent the display of one eBug
 * @param {Integer} robotId - Id of the Robot (to be displayed in its center)
 * @param {Number} originalPositionX - Starting x position
 * @param {Number} originalPositionY - Starting y position
 * @param {Number} originalAngle - Starting orientation in degrees
 * @param {Number} robotWidth - Size of the Robot
 * @param {String} robotColor - Color of the robot's display, either hexadecimal code or name of the color
 * @param {Number} [textSize=20] - Size of the Id's display
 * @param {String} triangleColor - Color of the triangle indicating the orientation
 * @param {Object} p5 - p5 library object
 * @param {Object} options - object of options, currently in use only for options.trackingTimeout, which
 * is the timeout between two positions being recorded for tracking
 */
export class Robot {
    constructor(robotId, originalPositionX, originalPositionY, originalAngle,
                robotWidth, robotColor, textSize, triangleColor, p5, options) {
        this.p = p5;

        this.position = {x: originalPositionX, y: originalPositionY};
        this.angle = originalAngle;
        this.id = robotId;
        this.triangle = {baseCenter: {x: null, y: null}, color: triangleColor || "red"};
        this.width = robotWidth;
        this.radius = robotWidth / 2;
        this.reducedRadius = (this.radius * 9) / 22.5;
        this.backgroundColor = robotColor;
        this.textSize = textSize || 20;
        this.textOffset = (6 * this.textSize) / 20;

        this.gradient = false;
        this.tracking = false;
        this.trackingCount = 0;
        this.trackingTimeout = options.trackingTimeout || TRACKING_TIMEOUT;
        this.trackedPositionManager = new RobotTrackedPositionManager(this.p, this);
        this.gradientManager = new Gradient(this.p, this);

        this.getRadAngle = function () {
            return this.angle * (Math.PI / 180);
        };

        this.calcTrianglePositions();

    }

    /**
     * @method moveTo
     * @desc Method to change the position and angle of the robot
     * @param {Number} newPositionX - New x position
     * @param {Number} newPositionY - New y position
     * @param {Number} angle - New orientation in degrees
     */
    moveTo(newPositionX, newPositionY, angle) {
        this.position.x = newPositionX;
        this.position.y = newPositionY;
        if (angle !== -1)
            this.angle = angle;

        this.calcTrianglePositions();
        if (this.tracking) {
            if ((this.trackingCount % this.trackingTimeout) === 0)
                this.trackedPositionManager.addPosition(newPositionX, newPositionY);
            this.trackingCount++;
        }
    }

    /**
     * @method calcTrianglePositions
     * @desc Updates the positions of the points of the triangle indicating orientation
     */
    calcTrianglePositions() {
        this.triangle.baseCenter.x = this.position.x + Math.sin(this.getRadAngle()) * this.reducedRadius;
        this.triangle.baseCenter.y = this.position.y - Math.cos(this.getRadAngle()) * this.reducedRadius;
    }

    /**
     * @method drawMainElements
     * @desc Draws the gradient if necessary, the border, the circle, the number and the triangle (the whole robot actually)
     */
    drawMainElements() {
        if (this.gradient)
            this.drawGradient();

        this.drawBorder();
        this.drawCircle();
        this.drawNumber();
        this.drawTriangle();
    }

    /**
     * @method drawCircle
     * @desc Draws the circle representing the robot
     */
    drawCircle() {
        this.p.fill(this.backgroundColor);
        this.p.ellipse(this.position.x, this.position.y, this.width);
    }

    /**
     * @method drawBorder
     * @desc Draws the border of the robot
     */
    drawBorder() {
        this.p.fill(this.triangle.color);
        this.p.ellipse(this.position.x, this.position.y, this.width + 5);
    }

    /**
     * @method drawTriangle
     * @desc Draws the triangle indicating the robot's orientation
     */
    drawTriangle() {
        this.p.push();

        this.p.fill(this.triangle.color);

        this.p.translate(this.triangle.baseCenter.x, this.triangle.baseCenter.y);
        this.p.rotate(this.getRadAngle());
        this.p.triangle(x1, y1, x2, y2, x3, y3);

        this.p.pop();
    }

    /**
     * @method drawNumber
     * @desc Draws the id of the robot into it
     */
    drawNumber() {
        this.p.push();

        this.p.fill(this.triangle.color);

        this.p.textSize(this.textSize);
        this.p.text(this.id, this.position.x - this.textOffset, this.position.y + this.textOffset);

        this.p.pop();
    }

    /**
     * @method drawGradient
     * @desc Draws the robot gradient using the robot's gradient manager
     */
    drawGradient() {
        this.gradientManager.draw();
    }

    /**
     * @method switchGradient
     * @desc Unable/disable the display of the gradient from the robot
     */
    switchGradient() {
        this.gradient = !this.gradient;
    }

    /**
     * @method switchGradient
     * @desc Unable/disable the display of the tracked positions from the robot (But not from the general manager)
     */
    switchTracking() {
        this.tracking = !this.tracking;
    }

    /**
     * @method jsonSerialize
     * @desc Serialize all the information in the Robot object into a javascript object (json-like)
     * @returns {{genRobotInfo: {id: Integer, width: Number, radius: Number, backgroundColor: String, textSize: Number, textOffset: Number}, currRobotInfo: {position: {x: Number, y: Number}, angle: Number, triangle: {baseCenter: {x: Number, y: Number}, color: String}}, actionsInfo: {gradient: Boolean, tracking: Boolean, trackingCount: Number, trackingTimeout: Number, trackedPositionManager: {robotWidth, startPositionIndex, lifespan, trackedPositions}}}}
     */
    jsonSerialize() {
        let robotCurrentInfo = {
            position: this.position,
            angle: this.angle,
            triangle: this.triangle
        };

        let robotGenInfo = {
            id: this.id,
            width: this.width,
            radius: this.radius,
            backgroundColor: this.backgroundColor,
            textSize: this.textSize,
            textOffset: this.textOffset
        };

        let actionsOnGoing = {
            gradient: this.gradient,
            tracking: this.tracking,
            trackingCount: this.trackingCount,
            trackingTimeout: this.trackingTimeout,
            trackedPositionManager: this.trackedPositionManager.jsonSerialize()
        };

        return {genRobotInfo: robotGenInfo, currRobotInfo: robotCurrentInfo, actionsInfo: actionsOnGoing};
    }
}
