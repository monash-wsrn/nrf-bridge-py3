/**
 * Created by tanguy on 03/04/17.
 */

import {redToYellowGradient} from './color'
let GRADIENT_RADIUS = 100;

export class GradientManager {
    constructor() {
        this.gradients = [];
    }

    addGradient(gradient) {
        this.gradients.push(gradient);
    }

    checkGradient(id, x, y) {
        let distance;

        this.gradients.forEach((element) => {
            if (id !== element.robot.id) {
                distance = Math.sqrt(Math.pow((element.robot.position.x - x), 2) + Math.pow((element.robot.position.y - y), 2))

                if (distance <= 100)
                    if (distance <= 50)
                        console.log("Robot " + id + " crashed into robot " + element.robot.id + " !");
                    else
                        console.log("Robot " + id + " is getting close to robot " + element.robot.id + ", be careful !");
            }
        });
    }
}

export class Gradient {
    constructor(p, robot, radius, gradColors) {
        this.p = p;
        this.robot = robot;

        this.radius = radius || GRADIENT_RADIUS;
        this.gradColors = gradColors || redToYellowGradient;
    }

    draw() {
        for (let r = this.radius; r > 0; --r) {
            this.p.fill(this.gradColors[r]);
            this.p.ellipse(this.robot.position.x, this.robot.position.y, r, r);
        }
    }
}
