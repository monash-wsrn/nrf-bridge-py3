# Client-Side eBugs Swarm Documentation

This javascript application is based on [p5.js](https://p5js.org/) (javascript processing implementation). It uses [webpack](https://webpack.github.io/docs/) to build the files.

## Table of Contents

- [Client-Side eBugs Swarm Documentation : Instructions](#client-side-ebugs-swarm-documentation---instructions)
  * [Getting Started: User](#getting-started--user)
  * [Getting Started: Developer](#getting-started--developer)
- [Client-Side eBugs Swarm Documentation : Developer Documentation](#client-side-ebugs-swarm-documentation---developer-documentation)
  * [RobotManager](#robotmanager)
    + [addRobot](#addrobot)
    + [getRobot](#getrobot)
    + [moveRobot](#moverobot)
    + [getRobotFactory](#getrobotfactory)
    + [drawAll](#drawall)
    + [switchGradientMode](#switchgradientmode)
    + [switchTrackingMode](#switchtrackingmode)
    + [switchSpyingMode](#switchspyingmode)
    + [afterMoveActions](#aftermoveactions)
    + [sendSpiedInfo](#sendspiedinfo)
  * [RobotFactory](#robotfactory)
    + [getRobot](#getrobot-1)
  * [Robot](#robot)
    + [moveTo](#moveto)
    + [calcTrianglePositions](#calctrianglepositions)
    + [drawMainElements](#drawmainelements)
    + [drawCircle](#drawcircle)
    + [drawBorder](#drawborder)
    + [drawTriangle](#drawtriangle)
    + [drawNumber](#drawnumber)
    + [drawGradient](#drawgradient)
    + [switchGradient](#switchgradient)
    + [switchGradient](#switchgradient-1)
    + [jsonSerialize](#jsonserialize)
  * [TrackedPositionManager](#trackedpositionmanager)
    + [drawAll](#drawall-1)
    + [addTracker](#addtracker)
  * [RobotTrackedPositionManager](#robottrackedpositionmanager)
    + [addPosition](#addposition)
    + [removePosition](#removeposition)
    + [drawAll](#drawall-2)
    + [drawParticular](#drawparticular)
    + [getNumberOfTrackedPositions](#getnumberoftrackedpositions)
    + [jsonSerialize](#jsonserialize-1)
  * [TrackedPosition](#trackedposition)
    + [draw](#draw)
    + [fading](#fading)
    + [jsonSerialize](#jsonserialize-2)
  * [GradientManager](#gradientmanager)
    + [addGradient](#addgradient)
    + [CheckGradient](#checkgradient)
  * [Gradient](#gradient)
    + [draw](#draw-1)
  * [getGradientHexa](#getgradienthexa)
  * [Button](#button)
    + [setAction](#setaction)
  * [ButtonCond](#buttoncond)
  * [WebsocketConnection](#websocketconnection)
    + [closeConnection](#closeconnection)
    + [send](#send)
    + [createConnection](#createconnection)

# Client-Side eBugs Swarm Documentation : Instructions

## Getting Started: User
As a user, you just need to clone the project, and a web browser !
(Keep in mind that the current state of the application supposes that you are running the webService on your machine,
otherwise you would need a little change in the code)

Then browse to the file `./web/static/index.html`, you're there !
(Don't hesitate to refresh the page if the connection to the server has failed, it triggers one when the page loads)
## Getting Started: Developer

As a developer, you'll need to install a few things to start working on this app:
1. Install [node.js](https://nodejs.org/en/) and [npm](https://www.npmjs.com/): `sudo apt-get install nodejs npm`
2. Clean npm cache: `sudo npm cache clean -f`
3. Install globally a node helper (used to upgrade node via npm): `sudo npm install -g n`
4. Upgrade your node version to the lts one (with support) using it: `sudo n lts`
5. Move to the `/client` directory
6. Install the modules: `npm install` (It may take a few minutes)

Then you can start working using `npm start` in the `/client` directory and browsing to `http://localhost:8080/`.
To build the production version (min.js file) use `npm run build`.

<!-- Generated by documentation.js. Update this documentation by updating the source code. -->

# Client-Side eBugs Swarm Documentation : Developer Documentation

## RobotManager

Main RobotManager knowing about all the Robots and the factories (should probably be a singleton)

**Parameters**

-   `p5` **p5** p5 library object
-   `onSpy` **[Function](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/function)** Function to call when spying is activated and a robot moves (optional, default `false`)

### addRobot

Adds a robot to the manager, should be called automatically by factories when they create a Robot

**Parameters**

-   `robot` **[Robot](#robot)** Robot object created by a robot factory

### getRobot

Gets a robot by id

**Parameters**

-   `id` **Integer** Id of the robot searched

Returns **([Robot](#robot) | null)** 

### moveRobots

Moves several robots using a javascript object

**Parameters**

-   `robotsLikeArray` **Array** Array of objects containing id, x, y and angle

### moveRobot

Move a robot

**Parameters**

-   `id` **Integer** Id of the robot to move
-   `x` **[Number](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number)** New position x
-   `y` **[Number](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number)** New position y
-   `angle` **[Number](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number)** New orientation in degrees

### getRobotFactory

Returns a new RobotFactory

**Parameters**

-   `params` **[object](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object)** Object containing all the params of the Factory (cf RobotFactory Class) (optional, default `{}`)

Returns **[RobotFactory](#robotfactory)** 

### drawAll

Draws everything !

### switchGradientMode

Unable/Disable gradients

### switchTrackingMode

Unable/Disable position tracking

### switchSpyingMode

Unable/Disable spying

### afterMovesActions

Place to trigger all the mehtods that should be called after a move of all the robots

### afterMoveActions

Place to trigger all the methods that should be called after a move

**Parameters**

-   `id` **Integer** Id of the moving robot
-   `x` **[Number](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number)** New position x
-   `y` **[Number](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number)** New position y
-   `angle` **[Number](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number)** New orientation

### sendSpiedInfo

Method to send to onSpy the data gathered "spying" robots

## RobotFactory

**Parameters**

-   `p5` **p5** p5 library object
-   `params` **[object](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object)** Parameters of the RobotFactory : robotWidth, robotColor, textSize, triangleColor, options (optional, default `{}`)
-   `addRobot` **[Function](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/function)** Function to addRobot to the manager

### getRobot

Creates a Robot object using the parameters of the factory

**Parameters**

-   `robotId` **[String](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String)** Id of the Robot
-   `originalPositionX` **[Number](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number)** Original position x
-   `originalPositionY` **[Number](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number)** Original position y
-   `originalAngle` **[Number](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number)** Original orientation in degrees

Returns **[Robot](#robot)** 

## Robot

Class to represent the display of one eBug

**Parameters**

-   `robotId` **Integer** Id of the Robot (to be displayed in its center)
-   `originalPositionX` **[Number](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number)** Starting x position
-   `originalPositionY` **[Number](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number)** Starting y position
-   `originalAngle` **[Number](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number)** Starting orientation in degrees
-   `robotWidth` **[Number](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number)** Size of the Robot
-   `robotColor` **[String](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String)** Color of the robot's display, either hexadecimal code or name of the color
-   `textSize` **[Number](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number)** Size of the Id's display (optional, default `20`)
-   `triangleColor` **[String](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String)** Color of the triangle indicating the orientation
-   `p5` **[Object](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object)** p5 library object
-   `options` **[Object](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object)** object of options, currently in use only for options.trackingTimeout, which
    is the timeout between two positions being recorded for tracking

### moveTo

Method to change the position and angle of the robot

**Parameters**

-   `newPositionX` **[Number](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number)** New x position
-   `newPositionY` **[Number](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number)** New y position
-   `angle` **[Number](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number)** New orientation in degrees

### calcTrianglePositions

Updates the positions of the points of the triangle indicating orientation

### drawMainElements

Draws the gradient if necessary, the border, the circle, the number and the triangle (the whole robot actually)

### drawCircle

Draws the circle representing the robot

### drawBorder

Draws the border of the robot

### drawTriangle

Draws the triangle indicating the robot's orientation

### drawNumber

Draws the id of the robot into it

### drawGradient

Draws the robot gradient using the robot's gradient manager

### switchGradient

Unable/disable the display of the gradient from the robot

### switchGradient

Unable/disable the display of the tracked positions from the robot (But not from the general manager)

### jsonSerialize

Serialize all the information in the Robot object into a javascript object (json-like)

Returns **{genRobotInfo: {id: Integer, width: [Number](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number), radius: [Number](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number), backgroundColor: [String](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String), textSize: [Number](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number), textOffset: [Number](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number)}, currRobotInfo: {position: {x: [Number](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number), y: [Number](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number)}, angle: [Number](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number), triangle: {baseCenter: {x: [Number](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number), y: [Number](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number)}, color: [String](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String)}}, actionsInfo: {gradient: [Boolean](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Boolean), tracking: [Boolean](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Boolean), trackingCount: [Number](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number), trackingTimeout: [Number](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number), trackedPositionManager: {robotWidth, startPositionIndex, lifespan, trackedPositions}}}** 

## TrackedPositionManager

Global manager for the RobotTrackedPositionManagers

## resetTracking

Resets the tracking in all the RobotTrackedPositionManagers

### drawAll

Draws all the tracked positions respecting their order of appearance (older ones first)

### addTracker

Adds a RobotTrackedPositionManager to follow

**Parameters**

-   `tracker` **[RobotTrackedPositionManager](#robottrackedpositionmanager)** 

## RobotTrackedPositionManager

Tracked positions manager for a single robot

**Parameters**

-   `p5` **p5** p5 library object
-   `robot` **[Robot](#robot)** Robot to keep track of positions
-   `lifespan` **[Number](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number)** Time the tracked positions stay on screen (not in seconds but in terms of number of executions) (optional, default `500`)

### addPosition

Adds a new tracked position to the tracker

**Parameters**

-   `x` **[Number](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number)** Tracked position x
-   `y` **[Number](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number)** Tracked position y

### removePosition

Removes the last tracked position from the tracker

### drawAll

Draws all the tracked positions within the manager consecutively (Not used currently)

### drawParticular

Draws a particular tracked position from its number (1, 2, 3...)

**Parameters**

-   `number` **[Number](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number)** Index of the tracked position to draw (first is 1)

### getNumberOfTrackedPositions

Returns the number of tracked positions within the manager

Returns **[number](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number)** 

### cleanTracker 

Removes the faded positions from the tracker, they are no longer referenced

### resetTracking

Reset the tracked positions by erasing everything

### jsonSerialize

Serialize all the information in the RobotTrackedPositionManager object into a javascript object (json-like)

Returns **{robotWidth: [Number](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number), startPositionIndex: [Number](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number), lifespan: [Number](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number), trackedPositions: [Array](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array)}** 

## TrackedPosition

A single tracked position of a robot

**Parameters**

-   `p5` **p5** p5 library object
-   `x` **[Number](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number)** The position x
-   `y` **[Number](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number)** The position y
-   `width` **[Number](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number)** The position width
-   `lifespan` **Integer** The number of times the position will be displayed before fading completely
-   `colorGradient` **[Array](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array)** Array of strings hexadecimal colors for the fading of the position
-   `removeTrack` **[Function](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/function)** Function to call to remove the tracked position from its manager
-   `fading` **[Boolean](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Boolean)** If the position is fading or not (optional, default `True`)

### draw

Draws the tracked position with the appropriate color

### fading

Reduces the index of the color in the gradient vector by one, making the color of the tracked position fade

### jsonSerialize

Serialize all the information in the TrackedPosition object into a javascript object (json-like)

Returns **{position: {x: [Number](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number), y: [Number](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number)}, width: [Number](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number), lifespan: Integer}** 

## GradientManager

Manager of all the gradients, used to check if they are touching one another

### addGradient

Adds a gradient to the manager

**Parameters**

-   `gradient` **[Gradient](#gradient)** 

### CheckGradient

Checks if the moving robot passed as parameter is getting close to another robot, if so console.logs a message

**Parameters**

-   `id` **[Number](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number)** Id of the robot which is moving
-   `x` **[Number](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number)** New position x
-   `y` **[Number](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number)** New position y

## Gradient

Object representing a gradient around a robot

**Parameters**

-   `p5` **p5** p5 library object
-   `robot` **[Robot](#robot)** The robot object concerned by the gradient
-   `radius` **[Number](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number)** Radius of the gradient displayed (optional, default `100`)
-   `gradColors` **[Array](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array)** Colors of the gradient (optional, default `redToYellowGradient`)

### draw

Draws the gradient

## getGradientHexa

Generates a gradient between two colors in hexadecimal code format

**Parameters**

-   `startingColor` **[String](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String)** Color to start the gradient from (Hexadecimal code)
-   `endingColor` **[String](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String)** Color to end the gradient with (Hexadecimal code)
-   `nbColors` **Integer** Number of colors generated

Returns **[Array](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array)** Array of hexadecimal codes of colors

## Button

Base component for a button triggering an action

**Parameters**

-   `action` **[Function](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/function)** Action to trigger when the button is clicked (optional, default `false`)
-   `text` **[String](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String)** Label of the button
-   `buttonClass` **[String](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String)** Css class to apply to the button (optional, default `""`)

### setAction

Sets the action of the button as the provided function

**Parameters**

-   `action` **[Function](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/function)** Function to be triggered when clicking on the button

## ButtonCond

**Extends Button**

Class extending Button to implement two different labels switching when clicked

**Parameters**

-   `action` **[Function](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/function)** Action to trigger when the button is clicked
-   `text1` **[String](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String)** First label of the button
-   `text2` **[String](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String)** Second label of the button
-   `buttonClass` **[String](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String)** Css class to apply to the button (optional, default `""`)

## WebsocketConnection

Class to handle the connection to a webService using websockets, createConnection is meant to be used instead of the constructor

**Parameters**

-   `onOpen`  
-   `onMessage`  
-   `onClose`  
-   `onError`  
-   `connection`  

### closeConnection

Closes the websocket connection

### send

Sends data through the websocket

**Parameters**

-   `data` **any** data to be send

### createConnection

Starts a connection to the server and creates a WebsocketConnection object

**Parameters**

-   `consoleLogs` **[Boolean](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Boolean)** Console logs or not on errors (optional, default `false`)
-   `address` **[String](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String)** Address of the server to connect to (optional, default `"ws://127.0.0.1:8765/"`)
-   `onMessage` **[Function](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/function)** Function to call when receiving a message (optional, default `false`)
-   `onOpen` **[Function](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/function)** Function to call when opening a connection (optional, default `false`)
-   `onClose` **[Function](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/function)** Function to call when closing a connection (optional, default `false`)
-   `onError` **[Function](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/function)** Function to call when an error happens (optional, default `false`)

Returns **[WebsocketConnection](#websocketconnection)** 