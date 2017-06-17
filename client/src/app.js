//This file is the main application, and the rest of the sources are a library
//Which means that this is a particular way of doing things, but it could be used in various ways !

//See this more like an example of using the architecture, than a big guideline

let p5 = require('p5');
window.p5 = p5;

import {RobotManager} from "./robotManager"
import {ButtonCond} from "./actionButton"
import {WebsocketConnection} from "./websocketConnection"

// Setting up the html elements
let app = document.getElementById("app");

let canvasDiv = document.createElement("div");
let optionsDiv = document.createElement("div");
optionsDiv.className = "optionsDiv";
canvasDiv.className = "appCanvas";
canvasDiv.id = "appCanvas";

// Buttons
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
spyDiv.className = "spyDiv";
optionsDiv.appendChild(spyDiv);

//Adjusting canvas size to the window
let canvasWidth = window.getComputedStyle(canvasDiv).width;
canvasWidth = canvasWidth.substring(0, canvasWidth.length - 2);

let canvasHeight = window.getComputedStyle(canvasDiv).height;
canvasHeight = canvasHeight.substring(0, canvasHeight.length - 2);

canvasHeight = canvasHeight - 85;


let max_distance, RobotMan, RobotFact1, RobotFact2, posForSpeed = [], speeds = [];

// Defining the action to use when "spying" the robots
// There it computes the instant speed saving positions
let onSpy = (data) => {

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
                speed: Math.round((Math.sqrt(Math.pow((posForSpeed[index].newPosition.x - posForSpeed[index].oldPosition.x), 2)
                        + Math.pow((posForSpeed[index].newPosition.y - posForSpeed[index].oldPosition.y), 2)) / 0.5) * 100) / 100,
                angle: elem.robotInfo.currRobotInfo.angle
            }
            ;
        });
    }

    spyDiv.textContent = JSON.stringify(speeds);
};

//Creating the sketch
let sketch = (p) => {

    //One Robot manager and two factories
    //It couldn't have been done before because we need to initialize the RobotManager with p, so within the sketch
    //Doing the same as with buttons with a "setP5" function would definitely be possible though
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

    //Updating the buttons actions
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

    let firstMessage = true;

    let onMessage = function (msg) {
        let dataArray = JSON.parse(msg.data);

        //If it's the firstMessage we create the objects, if not we just update the positions
        dataArray.forEach((element, index, array) => {
            array[index].x *= (canvasWidth / 1000);
            array[index].y *= (canvasHeight / 1000);

            if (firstMessage) {
                //Arbitrarily setting half of the robots on each factory
                if ((index % 2) === 0)
                    RobotFact1.getRobot(element.id, element.x, element.y, element.angle);
                else
                    RobotFact2.getRobot(element.id, element.x, element.y, element.angle);
            }
        });
        if(!firstMessage)
            RobotMan.moveRobots(dataArray);

        firstMessage = false
    };

    websocket = WebsocketConnection.createConnection(false, onMessage);

});

//Closing it before unload
window.addEventListener("beforeunload", function (event) {
    event.preventDefault();
    websocket.closeConnection();
});
