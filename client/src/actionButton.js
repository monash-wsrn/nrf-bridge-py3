/**
 * Created by tanguy on 13/03/17.
 */

// Base Component for a button triggering an action
export class Button {
    constructor(action, text, buttonClass) {
        this.element = document.createElement("button");
        this.element.className += " button";
        this.element.onmousedown = action;
        this.element.textContent = text;

        if(buttonClass)
            this.element.className += " " + buttonClass;
    }

    setAction(action){
        this.element.onmousedown = action;
    }

}

// Extending Button class with the possibility to change the displayed text between two options
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
