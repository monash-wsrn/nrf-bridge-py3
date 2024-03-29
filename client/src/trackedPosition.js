import {getGradientHexa} from './color'
import * as constants from './constants'

/**
 * @class TrackedPositionManager
 * @desc Global manager for the RobotTrackedPositionManagers
 */
export class TrackedPositionManager {
    constructor() {
        this.trackers = [];
        this.resetTrackersCount = 0;
        this.resetTrackersTimeout = 100;
    }

    /**
     * @method resetTracking
     * @desc resetTracking in all the RobotTrackedPositionManagers
     */
    resetTracking() {
        this.trackers.forEach((element) => element.resetTracking());
    }

    /**
     * @method drawAll
     * @desc Draws all the tracked positions respecting their order of appearance (older ones first)
     */
    drawAll() {
        this.resetTrackersCount++;

        let numberOfTracked = [];
        this.trackers.forEach((element) => {
            numberOfTracked.push(element.getNumberOfTrackedPositions());
            if (this.resetTrackersCount % this.resetTrackersTimeout === 0) element.cleanTracker();
        });

        let nMax = Math.max(...numberOfTracked);

        for (let j = 0; j < nMax; j++)
            for (let i = 0; i < this.trackers.length; i++)
                if (numberOfTracked[i] > j)
                    this.trackers[i].drawParticular(j);
    }

    /**
     * @method addTracker
     * @desc Adds a RobotTrackedPositionManager to follow
     * @param {RobotTrackedPositionManager} tracker
     */
    addTracker(tracker) {
        this.trackers.push(tracker);
    }
}

/**
 * @class RobotTrackedPositionManager
 * @desc Tracked positions manager for a single robot
 * @param {p5} p5 - p5 library object
 * @param {Robot} robot - Robot to keep track of positions
 * @param {Number} [lifespan=500] - Time the tracked positions stay on screen (not in seconds but in terms of number of executions)
 * @param {Number} [fadingTimeout=100] - Time elapsed between two fades of a tracked position
 */
export class RobotTrackedPositionManager {
    constructor(p5, robot, lifespan, fadingTimeout) {
        this.p5 = p5;
        this.width = robot.width;
        this.robotId = robot.id;

        this.lifespan = lifespan || constants.LIFESPAN;
        this.fadingTimeout = fadingTimeout || constants.FADING_TIMEOUT;

        this.colorGradient = getGradientHexa(robot.backgroundColor, "black", this.lifespan);

        this.startPositionIndex = 0;
        this.trackedPositions = [];
    }

    /**
     * @method addPosition
     * @desc Adds a new tracked position to the tracker
     * @param {Number} x - Tracked position x
     * @param {Number} y - Tracked position y
     */
    addPosition(x, y) {
        this.trackedPositions.push(new TrackedPosition(this.p5, x, y,
            this.width,
            this.lifespan,
            this.fadingTimeout,
            this.colorGradient,
            this.removePosition))
    }

    /**
     * @method removePosition
     * @desc Removes the last tracked position from the tracker
     */
    removePosition() {
        //The object isn't really destroyed, but as startPositionIndex advances it won't be drawn anymore
        this.startPositionIndex++;
    }

    /**
     * @method drawAll
     * @desc Draws all the tracked positions within the manager consecutively (Not used currently)
     */
    drawAll() {
        for (let i = this.startPositionIndex; i < this.trackedPositions.length; i++)
            this.trackedPositions[i].draw();
    }

    /**
     * @method drawParticular
     * @desc Draws a particular tracked position from its number (1, 2, 3...)
     * @param {Number} number - Index of the tracked position to draw (first is 1)
     */
    drawParticular(number) {
        this.trackedPositions[number + this.startPositionIndex].draw();
    }

    /**
     * @method getNumberOfTrackedPositions
     * @desc Returns the number of tracked positions within the manager
     * @returns {number}
     */
    getNumberOfTrackedPositions() {
        return this.trackedPositions.length - this.startPositionIndex;
    }

    /**
     * @method cleanTracker
     * @desc Removing the faded positions from the tracker, they are no longer referenced
     */
    cleanTracker() {
        this.trackedPositions = this.trackedPositions.slice(this.startPositionIndex);
        this.startPositionIndex = 0;
    }

    /**
     * @method resetTracking
     * @desc Reset the tracked positions by erasing everything
     */
    resetTracking() {
        this.trackedPositions = [];
        this.startPositionIndex = 0;
    }

    /**
     * @method jsonSerialize
     * @desc Serialize all the information in the RobotTrackedPositionManager object into a javascript object (json-like)
     * @returns {{robotWidth: Number, startPositionIndex: Number, lifespan: Number, trackedPositions: Array}}
     */
    jsonSerialize() {
        return {
            robotWidth: this.width,
            startPositionIndex: this.startPositionIndex,
            lifespan: this.lifespan,
            trackedPositions: this.trackedPositions.slice(0).map((elem) => {
                return elem.jsonSerialize();
            })
        }
    }
}

/**
 * @class TrackedPosition
 * @desc A single tracked position of a robot
 * @param {p5} p5 - p5 library object
 * @param {Number} x - The position x
 * @param {Number} y - The position y
 * @param {Number} width - The position width
 * @param {Integer} lifespan - The number of times the position will be displayed before fading completely
 * @param {Number} fadingTimeout - Time elapsed between two fades of a tracked position
 * @param {Array} colorGradient - Array of strings hexadecimal colors for the fading of the position
 * @param {Function} removeTrack - Function to call to remove the tracked position from its manager
 * @param {Boolean} [fading=True] - If the position is fading or not
 */
class TrackedPosition {
    constructor(p5, x, y, width, lifespan, fadingTimeout, colorGradient, removeTrack, fading = true) {
        this.p5 = p5;
        this.position = {x: x, y: y};
        this.width = 0.75 * width;
        this.lifespan = lifespan;
        this.fadingTimeout = fadingTimeout;
        this.colorGradient = colorGradient;

        this.removePosition = removeTrack;
        this.fading = this.fading.bind(this);

        if (fading)
            this.fading();
    }

    /**
     * @method draw
     * @desc Draws the tracked position with the appropriate color
     */
    draw() {
        let col = this.colorGradient[this.lifespan];
        this.p5.fill(col);
        this.p5.ellipse(this.position.x, this.position.y, this.width);
    }

    /**
     * @method fading
     * @desc Reduces the index of the color in the gradient vector by one, making the color of the tracked position fade
     */
    fading() {
        this.lifespan--;
        if (this.lifespan > 0)
            setTimeout(this.fading, this.fadingTimeout);
        else
            this.removePosition();
    }

    /**
     * Serialize all the information in the TrackedPosition object into a javascript object (json-like)
     * @returns {{position: {x: Number, y: Number}, width: Number, lifespan: Integer}}
     */
    jsonSerialize() {
        return {position: this.position, width: this.width, lifespan: this.lifespan}
    }
}
