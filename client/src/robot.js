/**
 * Created by tanguy on 13/03/17.
 */

import {RobotTrackedPositionManager} from "./trackedPosition"
import {Gradient} from "./gradient"

//Triangle constants
let ROBOT_TRIANGLE_HEIGHT = Math.sqrt((16 * 16) - 64);
let x1 = -8, y1 = 0, x2 = 8, y2 = 0, x3 = 0, y3 = -ROBOT_TRIANGLE_HEIGHT;

//Options Constants
let TRACKING_TIMEOUT = 24;


export class Robot {

    constructor(robotName, originalPositionX, originalPositionY, originalAngle,
                robotWidth, robotColor, textSize, triangleColor, p5, options) {
        this.p = p5;

        this.position = {x: originalPositionX, y: originalPositionY};
        this.angle = originalAngle;
        this.name = String(robotName);
        this.triangle = {baseCenter: {x: null, y: null}, color: triangleColor || "red"};
        this.width = robotWidth;
        this.radius = robotWidth/2;
        this.reducedRadius = (this.radius*9)/22.5;
        this.backgroundColor = robotColor;
        this.textSize = textSize || 20;
        this.textOffset = (6*this.textSize)/20;

        this.gradient = false;
        this.tracking = false;
        this.trackingCount = 0;
        this.trackingTimeout = options.trackingTimeout || TRACKING_TIMEOUT;
        this.trackedPositionManager = new RobotTrackedPositionManager(this.p, this);
        this.gradientManager = new Gradient(this.p, this);

        this.getRadAngle = function(){
            return this.angle * (Math.PI/180);
        };

        this.calcTrianglePositions();

    }

    moveTo(newPositionX, newPositionY, angle) {
        this.position.x = newPositionX;
        this.position.y = newPositionY;
        if (angle !== -1)
            this.angle = angle;

        this.calcTrianglePositions();
        if(this.tracking) {
            if((this.trackingCount % this.trackingTimeout) === 0)
                this.trackedPositionManager.addPosition(newPositionX, newPositionY);
            this.trackingCount++;
        }
    }

    calcTrianglePositions(){
        this.triangle.baseCenter.x = this.position.x + Math.sin(this.getRadAngle())*this.reducedRadius;
        this.triangle.baseCenter.y = this.position.y - Math.cos(this.getRadAngle())*this.reducedRadius;
    }

    drawMainElements(){
        if(this.gradient)
            this.drawGradient();

        this.drawBorder();
        this.drawCircle();
        this.drawNumber();
        this.drawTriangle();
    }

    drawCircle(){
        this.p.fill(this.backgroundColor);
        this.p.ellipse(this.position.x, this.position.y, this.width);
    }

    drawBorder(){
        this.p.fill(this.triangle.color);
        this.p.ellipse(this.position.x, this.position.y, this.width + 5);
    }

    drawTriangle(){
        this.p.push();

        this.p.fill(this.triangle.color);

        this.p.translate(this.triangle.baseCenter.x, this.triangle.baseCenter.y);
        this.p.rotate(this.getRadAngle());
        this.p.triangle(x1, y1, x2, y2, x3, y3);

        this.p.pop();
    }

    drawNumber(){
        this.p.push();

        this.p.fill(this.triangle.color);

        this.p.textSize(this.textSize);
        this.p.text(this.name, this.position.x - this.textOffset, this.position.y + this.textOffset);

        this.p.pop();
    }

    drawGradient(){
        this.gradientManager.draw();
    }

    switchGradient(){
        this.gradient = !this.gradient;
    }

    switchTracking(){
        this.tracking = !this.tracking;
    }

    jsonSerialize(){
        let robotCurrentInfo = {
            position: this.position,
            angle: this.angle,
            triangle: this.triangle
        };

        let robotGenInfo = {
            name: this.name,
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
