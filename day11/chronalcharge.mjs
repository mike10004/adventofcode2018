/*
 * module chronalcharge 
 */

const SUM = (a, b) => a + b;

export class Position {
    constructor(x, y) {
        this.x = x;
        this.y = y;
    }

    static parse(text) {
        const values = text.split(/\s*,\s*/).slice(0).map(t => parseInt(t, 10));
        return new Position(values[0], values[1]);
    }

    toString() {
        return this.x + "," + this.y.toString();
    }
}

export class FuelCell {

    static getHundredsDigit(value) {
        value = (value % 1000);
        return parseInt(value / 100);
    }

    static findPowerLevel(x, y, serialNumber) {
        const rackId = x + 10;
        let power = rackId * y;
        power += serialNumber;
        power *= rackId;
        return FuelCell.getHundredsDigit(power) - 5;
    }

}

function toKey(x, y) {
    return x + "," + y;
}

export class Grid {
    
    constructor(coordMin, coordMax, serialNumber, verbose) {
        this.coordMin = coordMin;
        this.coordMax = coordMax;
        this.serialNumber = serialNumber;
        this.verbose = verbose;
    }

    toString() {
        return JSON.stringify(this);
    }

    contains(x, y) {
        return x >= this.coordMin && x <= this.coordMax && y >= this.coordMin && y <= this.coordMax;
    }

    powerLevelAt(x, y) {
        return FuelCell.findPowerLevel(x, y, this.serialNumber);
    }

    /**
     * Compute the sum of power levels in a square.
     * @param {number} x x-coordinate of the square
     * @param {number} y y-coordinate of the square
     * @param {number} squareSize square size
     * @param {Map} previous a map of "x,y" to power sums at (squareSize - 1)
     */
    sumPowerLevels(x, y, squareSize, previous) {
        const subSquareSum = previous.get(toKey(x, y));
        if (typeof(subSquareSum) === 'undefined' && squareSize !== 1) {
            throw new Error("previous power sum not already computed at squareSize = " + squareSize);
        }
        let borderSum = 0;
        for (let i = 0; i < squareSize; i++) { // right border
            borderSum += this.powerLevelAt(x + (squareSize - 1), y + i);
        }
        for (let i = 0; i < (squareSize - 1); i++) { // bottom border, except rightmost cell
            borderSum += this.powerLevelAt(x + i, y + (squareSize - 1));
        }
        return (subSquareSum || 0) + borderSum;
    }

    /**
     * 
     * @param {number} maxSquareSize the max square size to examine
     * @returns position of top-left square
     */
    findMaxPower(maxSquareSize) {
        let cornerPosition = null, maxPower = null;
        let previous = new Map(); // map of position to square power sum at previous square size
        for (let squareSize = 1; squareSize <= maxSquareSize; squareSize++) {
            const current = new Map(); 
            if (this.verbose) {
                console.debug("looking for max power with square size", squareSize);
            }
            for (let y = this.coordMin; y <= (this.coordMax - squareSize); y++) {
                for (let x = this.coordMin; x <= (this.coordMax - squareSize); x++) {
                    const powerSum = this.sumPowerLevels(x, y, squareSize, previous);
                    current.set(toKey(x, y), powerSum);
                    if (maxPower === null || powerSum > maxPower) {
                        maxPower = powerSum;
                        cornerPosition = new Position(x, y);
                        cornerPosition.squareSize = squareSize;
                    }
                }
            }
            previous = current;
        };
        return cornerPosition;
    }

}

export default {
    FuelCell: FuelCell,
};
