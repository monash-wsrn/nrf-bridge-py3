import Rainbow from 'rainbowvis.js';

/**
 * @function getGradientHexa
 * @desc Generates a gradient between two colors in hexadecimal code format
 * @param {String} startingColor - Color to start the gradient from (Hexadecimal code)
 * @param {String} endingColor - Color to end the gradient with (Hexadecimal code)
 * @param {Integer} nbColors - Number of colors generated
 * @returns {Array} - Array of hexadecimal codes of colors
 */
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
