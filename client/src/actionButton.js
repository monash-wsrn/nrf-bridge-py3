/**
 * @class Button
 * @desc Base component for a button triggering an action
 * @param {Function} [action=false] - Action to trigger when the button is clicked
 * @param {String} text - Label of the button
 * @param {String} [buttonClass=""] - Css class to apply to the button
 */
export class Button {
    constructor(action=()=>{}, text, buttonClass="") {
        this.element = document.createElement("button");
        this.element.className += " button";
        this.element.onmousedown = action;
        this.element.textContent = text;
        this.element.className += " " + buttonClass;
    }

    /**
     * @method setAction
     * @desc Sets the action of the button as the provided function
     * @param {Function} action - Function to be triggered when clicking on the button
     */
    setAction(action){
        this.element.onmousedown = action;
    }

}

/**
 * @class ButtonCond
 * @desc Class extending Button to implement two different labels switching when clicked
 * @param {Function} action - Action to trigger when the button is clicked
 * @param {String} text1 - First label of the button
 * @param {String} text2 - Second label of the button
 * @param {String} [buttonClass=""] - Css class to apply to the button
 */
export class ButtonCond extends Button {
    constructor(action, text1, text2, buttonClass) {
        super(action, text1, buttonClass);

        this.changeText = () => {
            this.element.textContent = this.element.textContent === text1 ? text2 : text1;
        };

        this.changeText = this.changeText.bind(this);

        this.element.onmouseup = this.changeText;
    }
}