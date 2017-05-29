/**
 * Created by tanguy on 27/03/17.
 */
import Rainbow from 'rainbowvis.js';


export const getGradientHexa = (startingColor, endingColor, nbColors) => {
    let rainbow = new Rainbow();
    let rainbowArray = [];
    rainbow.setNumberRange(0, nbColors);
    rainbow.setSpectrum(endingColor, startingColor);

    for (let i = 0; i <= nbColors; i++) {
        rainbowArray.push('#' + rainbow.colourAt(i))
    }

    return rainbowArray;
};

export const redToYellowGradient = getGradientHexa('#FFC914', '#ff0000', 100);
