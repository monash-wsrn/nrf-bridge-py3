/**
 * Created by tanguy on 03/04/17.
 */
import {getGradientHexa} from './color'

let LIFESPAN = 500;

export class TrackedPositionManager {
    constructor() {
        this.trackers = [];
    }
    drawAll(){
        let numberOfTracked = [];
        for (let i = 0; i < this.trackers.length; i++)
            numberOfTracked.push(this.trackers[i].getNumberOfTrackedPositions());

        let nMax = Math.max(...numberOfTracked);

        for(let j=0; j < nMax ;j++)
            for (let i = 0; i < this.trackers.length; i++)
                if(numberOfTracked[i]>j)
                    this.trackers[i].drawParticular(j);
    }
    addTracker(tracker){
        this.trackers.push(tracker);
    }
}

export class RobotTrackedPositionManager {
    constructor(p, robot, lifespan) {
        this.p = p;
        this.width = robot.width;

        this.colorGradient = getGradientHexa(robot.backgroundColor, "black", lifespan || LIFESPAN);

        this.startPositionIndex = 0;
        this.trackedPositions = [];
        this.lifespan = lifespan || LIFESPAN;
    }

    addPosition(x, y) {
        this.trackedPositions.push(new TrackedPosition(this.p, x, y,
            this.width,
            this.lifespan,
            this.colorGradient,
            this.removePosition))
    }

    removePosition() {
        this.startPositionIndex++;
    }

    drawAll() {
        for (let i = this.startPositionIndex; i < this.trackedPositions.length; i++)
            this.trackedPositions[i].draw();
    }

    drawParticular(number) {
        this.trackedPositions[number+this.startPositionIndex].draw();
    }

    getNumberOfTrackedPositions() {
        return this.trackedPositions.length - this.startPositionIndex;
    }

    jsonSerialize() {
        return {
            robotWidth: this.width,
            startPositionIndex: this.startPositionIndex,
            lifespan: this.lifespan,
            trackedPositions: this.trackedPositions.slice(0).map((elem)=>{
                return elem.jsonSerialize();
            })
        }
    }
}


class TrackedPosition {
    constructor(p, x, y, width, lifespan, colorGradient, removeTrack) {
        this.p = p;
        this.position = {x: x, y: y};
        this.width = 0.75 * width;
        this.lifespan = lifespan || LIFESPAN;
        this.colorGradient = colorGradient;

        this.removePosition = removeTrack;
        this.fading = this.fading.bind(this);

        this.fading();
    }

    draw() {
        let col = this.colorGradient[this.lifespan];
        this.p.fill(col);
        this.p.ellipse(this.position.x, this.position.y, this.width);
    }

    fading() {
        this.lifespan--;
        if (this.lifespan > 0)
            setTimeout(this.fading, 100);
        else
            this.removePosition();
    }

    jsonSerialize(){
        return {position: this.position, width: this.width, lifespan: this.lifespan}
    }
}
