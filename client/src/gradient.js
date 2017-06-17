import {redToYellowGradient} from './color'
let GRADIENT_RADIUS = 100;

/**
 * @class GradientManager
 * @desc Manager of all the gradients, used to check if they are touching one another
 */
export class GradientManager {
    constructor() {
        this.gradients = [];
    }

    /**
     * @method addGradient
     * @desc Adds a gradient to the manager
     * @param {Gradient} gradient
     */
    addGradient(gradient) {
        this.gradients.push(gradient);
    }

    /**
     * @method CheckGradient
     * @desc Checks if the moving robot passed as parameter is getting close to another robot, if so console.logs a message
     * @param {Number} id - Id of the robot which is moving
     * @param {Number} x - New position x
     * @param {Number} y - New position y
     */
    checkGradient(id, x, y) {
        let distance;

        this.gradients.forEach((element) => {
            if (id !== element.robot.id) {
                distance = Math.sqrt(Math.pow((element.robot.position.x - x), 2) + Math.pow((element.robot.position.y - y), 2))

                if (distance <= 125)
                    if (distance <= 50)
                        console.log("Robot " + id + " crashed into robot " + element.robot.id + " !");
                    else
                        console.log("Robot " + id + " is getting close to robot " + element.robot.id + ", be careful !");
            }
        });
    }
}

/**
 * @class Gradient
 * @desc Object representing a gradient around a robot
 * @param {p5} p5 - p5 library object
 * @param {Robot} robot - The robot object concerned by the gradient
 * @param {Number} [radius=100] - Radius of the gradient displayed
 * @param {Array} [gradColors=redToYellowGradient] - Colors of the gradient
 */
export class Gradient {
    constructor(p5, robot, radius, gradColors) {
        this.p5 = p5;
        this.robot = robot;

        this.radius = radius || GRADIENT_RADIUS;
        this.gradColors = gradColors || redToYellowGradient;
    }

    /**
     * @method draw
     * @desc Draws the gradient
     */
    draw() {
        for (let r = this.radius; r > 0; --r) {
            this.p5.fill(this.gradColors[r]);
            this.p5.ellipse(this.robot.position.x, this.robot.position.y, r, r);
        }
    }
}
