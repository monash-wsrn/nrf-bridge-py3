let p5 = require('p5');
window.p5 = p5;

import {RobotManager} from "./robotManager"
import {ButtonCond} from "./actionButton"
import {WebsocketConnection} from "./websocketConnection"

// Setting up the elements
let app = document.getElementById("app");

let canvasDiv = document.createElement("div");
let optionsDiv = document.createElement("div");
optionsDiv.className = "optionsDiv";
canvasDiv.className = "appCanvas";
canvasDiv.id = "appCanvas";

let button1 = new ButtonCond(() => {
}, "Enable Gradients", "Disable Gradients", "button1");
let button2 = new ButtonCond(() => {
}, "Enable Tracking", "Disable Tracking", "button2");
let button3 = new ButtonCond(() => {
}, "Enable Spying", "Disable Spying", "button3");

app.appendChild(canvasDiv);
app.appendChild(optionsDiv);
optionsDiv.appendChild(button1.element);
optionsDiv.appendChild(button2.element);
optionsDiv.appendChild(button3.element);

let spyDiv = document.createElement("div");
optionsDiv.appendChild(spyDiv);

let canvasWidth = window.getComputedStyle(canvasDiv).width;
canvasWidth = canvasWidth.substring(0, canvasWidth.length - 2);

let canvasHeight = window.getComputedStyle(canvasDiv).height;
canvasHeight = canvasHeight.substring(0, canvasHeight.length - 2);

canvasHeight = canvasHeight - 85;


let max_distance, RobotMan, RobotFact1, RobotFact2, posForSpeed = [], speeds = [];

// Defining the action to use when "spying" the robots
let onSpy = (data) => {
    // console.log(Object.assign({date: new Date()}, data));

    if (posForSpeed.length === 0) {
        data.forEach((elem, index) => {
            posForSpeed.push({
                oldPosition: {},
                newPosition: Object.assign({}, elem.robotInfo.currRobotInfo.position),
            });

            speeds.push({id: index, speed: "N.A", angle: elem.robotInfo.currRobotInfo.angle})
        });
    }


    else {
        data.forEach((elem, index) => {
            posForSpeed[index] = Object.assign(posForSpeed[index], {
                oldPosition: Object.assign({}, posForSpeed[index].newPosition),
                newPosition: Object.assign({}, elem.robotInfo.currRobotInfo.position)
            });

            speeds[index] = {
                id: index,
                speed: Math.round(Math.sqrt(Math.pow((posForSpeed[index].newPosition.x - posForSpeed[index].oldPosition.x), 2)
                        + Math.pow((posForSpeed[index].newPosition.y - posForSpeed[index].oldPosition.y), 2)) / 0.5, -2),
                angle: elem.robotInfo.currRobotInfo.angle
            }
            ;
        });
    }

    spyDiv.textContent = JSON.stringify(speeds);
};

//Creating the sketch
let sketch = (p) => {

    RobotMan = new RobotManager(p, onSpy);
    RobotFact1 = RobotMan.getRobotFactory({
        robotWidth: 55,
        robotColor: "#FF0000",
        triangleColor: "#008000"
    });

    RobotFact2 = RobotMan.getRobotFactory({
        robotWidth: 55,
        robotColor: "#008000",
        triangleColor: "#FF0000"
    });

    RobotFact1.getRobot(0, 20, 20, 100);
    RobotFact1.getRobot(1, 100, 100, 100);
    RobotFact1.getRobot(2, 300, 50, 145);

    RobotFact2.getRobot(3, 550, 200, 280);
    RobotFact2.getRobot(4, 800, 389, 300);
    RobotFact2.getRobot(5, 490, 50, 270);

    button1.setAction(() => RobotMan.switchGradientMode());
    button2.setAction(() => RobotMan.switchTrackingMode());
    button3.setAction(() => {
        spyDiv.textContent = "";
        RobotMan.switchSpyingMode();
    });

    p.setup = () => {
        let canvas = p.createCanvas(canvasWidth, canvasHeight);
        canvas.parent('appCanvas');

        p.noStroke();
        max_distance = p.dist(0, 0, canvasWidth, canvasHeight);

        p.frameRate(24);

        // p.noLoop();
    };

    p.draw = () => {
        p.background(0);

        RobotMan.drawAll();
    };

};

let myp5 = new p5(sketch);


let websocket;

//Setting the websocket connection on load
window.addEventListener("load", function () {

    let onMessage = function (msg) {
        let robotsArray = JSON.parse(msg.data);

        robotsArray.forEach((element) => {
            RobotMan.moveRobot(element.id - 1,
                element.x * canvasWidth / 1000,
                element.y * canvasHeight / 1000,
                element.angle);
        });
    };

    websocket = WebsocketConnection.createConnection(false, onMessage);

});

//Closing it before unload
window.addEventListener("beforeunload", function (event) {
    event.preventDefault();
    websocket.closeConnection();
});
