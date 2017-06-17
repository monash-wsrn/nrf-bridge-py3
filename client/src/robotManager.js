import {Robot} from "./robot"
import {TrackedPositionManager} from "./trackedPosition"
import {GradientManager} from "./gradient"

//Default constants
let ROBOT_WIDTH = 45;
let ROBOT_COLOR = "#FFFFFF";
let ROBOT_TEXT_SIZE = 20;
let ROBOT_TRIANGLE_COLOR = "#FF0000";

/**
 * @class RobotManager
 * @desc Main RobotManager knowing about all the Robots and the factories (should probably be a singleton)
 * @param {p5} p5 - p5 library object
 * @param {Function} [onSpy=false] - Function to call when spying is activated and a robot moves
 */
export class RobotManager {
    constructor(p5, onSpy = false) {
        this.p = p5;
        this.factories = [];
        this.robots = [];

        this.gradient = false;
        this.tracking = false;
        this.spying = false;

        this.trackedPositionManager = new TrackedPositionManager();
        this.gradientManager = new GradientManager();

        this.afterMoveTimeout = 0;

        if (onSpy)
            this.onSpy = onSpy;

        this.afterMoveActions = this.afterMoveActions.bind(this);
        this.addRobot = this.addRobot.bind(this);
    }

    /**
     * @method addRobot
     * @desc Adds a robot to the manager, should be called automatically by factories when they create a Robot
     * @param {Robot} robot - Robot object created by a robot factory
     */
    addRobot(robot) {
        this.trackedPositionManager.addTracker(robot.trackedPositionManager);
        this.gradientManager.addGradient(robot.gradientManager);

        this.robots.push(robot);
    }

    /**
     * @method getRobot
     * @desc Gets a robot by id
     * @param {Integer} id - Id of the robot searched
     * @returns {Robot|null}
     */
    getRobot(id) {
        return this.robots.find((element) => {
            return element.id === id
        })
    }

    /**
     * @method moveRobot
     * @desc Move a robot
     * @param {Integer} id - Id of the robot to move
     * @param {Number} x - New position x
     * @param {Number} y - New position y
     * @param {Number} angle - New orientation in degrees
     */
    moveRobot(id, x, y, angle) {
        let robot = this.getRobot(id);

        if (robot) {
            robot.moveTo(x, y, angle);
            this.afterMoveActions(id, x, y, angle);
        }
        else
            console.log("The Robot " + id + " doesn't exist")
    }

    /**
     * @method getRobotFactory
     * @desc Returns a new RobotFactory
     * @param {object} params - Object containing all the params of the Factory (cf RobotFactory Class)
     * @returns {RobotFactory}
     */
    getRobotFactory(params = {}) {
        let factory = new RobotFactory(this.p, params, this.addRobot);

        this.factories.push(factory);

        return factory;
    }

    /**
     * @method drawAll
     * @desc Draws everything !
     */
    drawAll() {
        if (this.tracking)
            this.trackedPositionManager.drawAll();
        // this.robots.forEach((element)=>element.drawSecondaryElements());
        this.robots.forEach((element) => element.drawMainElements());
    }

    /**
     * @method switchGradientMode
     * @desc Unable/Disable gradients
     */
    switchGradientMode() {
        this.gradient = !this.gradient;
        this.robots.forEach((element) => element.switchGradient());
    }

    /**
     * @method switchTrackingMode
     * @desc Unable/Disable position tracking
     */
    switchTrackingMode() {
        this.tracking = !this.tracking;
        this.robots.forEach((element) => element.switchTracking());
    }

    /**
     * @method switchSpyingMode
     * @desc Unable/Disable spying
     */
    switchSpyingMode() {
        this.spying = !this.spying;
    }

    /**
     * @method afterMoveActions
     * @desc Place to trigger all the methods that should be called after a move
     * @param {Integer} id - Id of the moving robot
     * @param {Number} x - New position x
     * @param {Number} y - New position y
     * @param {Number} angle - New orientation
     */
    afterMoveActions(id, x, y, angle) {
        this.afterMoveTimeout++;
        if ((Math.ceil(this.afterMoveTimeout/this.robots.length) % 50) === 0) {
            // this.factories.forEach((element)=>element.afterMoveActions(id, x, y, angle));
            if (this.gradient)
                this.gradientManager.checkGradient(id, x, y);
            if (this.spying) {
                this.sendSpiedInfo();
            }
        }
    }

    /**
     * @method sendSpiedInfo
     * @desc Method to send to onSpy the data gathered "spying" robots
     */
    sendSpiedInfo() {
        let data = this.robots.slice(0).map((elem, index) => {
            return {robotId: index, robotInfo: elem.jsonSerialize()};
        });

        this.onSpy(data);
    }
}

/**
 * @class RobotFactory
 * @param {p5} p5 - p5 library object
 * @param {object} [params={}] - Parameters of the RobotFactory : robotWidth, robotColor, textSize, triangleColor, options
 * @param {Function} addRobot - Function to addRobot to the manager
 */
export class RobotFactory {
    constructor(p5, params = {}, addRobot) {
        this.p = p5;
        this.robotWidth = params.robotWidth || ROBOT_WIDTH;
        this.robotColor = params.robotColor || ROBOT_COLOR;
        this.textSize = params.textSize || ROBOT_TEXT_SIZE;
        this.triangleColor = params.triangleColor || ROBOT_TRIANGLE_COLOR;
        this.options = params.options || {};

        // this.robots = [];

        this.addRobot = addRobot;
    }

    /**
     * @method getRobot
     * @desc Creates a Robot object using the parameters of the factory
     * @param {String} robotId - Id of the Robot
     * @param {Number} originalPositionX  - Original position x
     * @param {Number} originalPositionY - Original position y
     * @param {Number} originalAngle - Original orientation in degrees
     * @returns {Robot}
     */
    getRobot(robotId, originalPositionX, originalPositionY, originalAngle) {
        let robot = new Robot(robotId,
            originalPositionX,
            originalPositionY,
            originalAngle,
            this.robotWidth,
            this.robotColor,
            this.textSize,
            this.triangleColor,
            this.p,
            this.options);

        this.addRobot(robot);
        // this.robots.push(robot);

        return robot;
    }

    // afterMoveActions(id, x, y, angle){
    // }
}
