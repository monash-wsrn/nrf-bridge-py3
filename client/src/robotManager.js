/**
 * Created by tanguy on 10/04/17.
 */

import {Robot} from "./robot"
import {TrackedPositionManager} from "./trackedPosition"
import {GradientManager} from "./gradient"

//Default constants
let ROBOT_WIDTH = 45;
let ROBOT_COLOR = "#FFFFFF";
let ROBOT_TEXT_SIZE = 20;
let ROBOT_TRIANGLE_COLOR = "#FF0000";


export class RobotManager {
    constructor(p5, onSpy=false) {
        this.p = p5;
        this.factories = [];
        this.robots = [];

        this.gradient = false;
        this.tracking = false;
        this.spying = false;

        this.trackedPositionManager = new TrackedPositionManager();
        this.gradientManager = new GradientManager();

        this.afterMoveTimeout = 0;
        this.nextRobotId = 0;

        if(onSpy)
            this.onSpy = onSpy;

        this.afterMoveActions = this.afterMoveActions.bind(this);
        this.addRobot = this.addRobot.bind(this);
    }

    addRobot(robot){
        robot.id = this.nextRobotId++;
        this.trackedPositionManager.addTracker(robot.trackedPositionManager);
        this.gradientManager.addGradient(robot.gradientManager);

        this.robots.push(robot);
    }

    moveRobot(id, x, y, angle){
        this.robots[id].moveTo(x, y, angle);

        this.afterMoveActions(id, x, y, angle);
    }

    getRobotFactory(params={}){
        let factory = new RobotFactory(this.p, params, this.addRobot);

        this.factories.push(factory);

        return factory;
    }

    drawAll(){
        if(this.tracking)
            this.trackedPositionManager.drawAll();
        // this.robots.forEach((element)=>element.drawSecondaryElements());
        this.robots.forEach((element)=>element.drawMainElements());
    }

    switchGradientMode(){
        this.gradient = !this.gradient;
        this.robots.forEach((element)=>element.switchGradient());
    }

    switchTrackingMode(){
        this.tracking = !this.tracking;
        this.robots.forEach((element)=>element.switchTracking());
    }

    switchSpyingMode(){
        this.spying = !this.spying;
    }

    afterMoveActions(id, x, y, angle){
        this.afterMoveTimeout++;
        if((this.afterMoveTimeout % 50) === 0) {
            // this.factories.forEach((element)=>element.afterMoveActions(id, x, y, angle));
            if(this.gradient)
                this.gradientManager.checkGradient(id, x, y);
            if(this.spying) {
                this.sendSpyedInfo();
            }
        }
    }

    sendSpyedInfo(){
        let data = this.robots.slice(0).map((elem, index)=> {
            return {robotId: index, robotInfo: elem.jsonSerialize()};
        });

        this.onSpy(data);
    }
}

//Factory for Robots
export class RobotFactory {
    constructor(p5, params={}, addRobot) {
        this.p = p5;
        this.robotWidth = params.robotWidth || ROBOT_WIDTH;
        this.robotColor = params.robotColor || ROBOT_COLOR;
        this.textSize = params.textSize || ROBOT_TEXT_SIZE;
        this.triangleColor = params.triangleColor || ROBOT_TRIANGLE_COLOR;
        this.options = params.options || {};

        // this.robots = [];

        this.addRobot = addRobot;
    }

    getRobot(robotName, originalPositionX, originalPositionY, originalAngle) {
        let robot =  new Robot(robotName,
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
