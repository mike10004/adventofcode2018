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

export class Grid {
    
    constructor(coordMin, coordMax, serialNumber) {
        this.coordMin = coordMin;
        this.coordMax = coordMax;
        this.serialNumber = serialNumber;
    }

    toString() {
        return JSON.stringify(this);
    }

    contains(x, y) {
        return x >= this.coordMin && x <= this.coordMax && y >= this.coordMin && y <= this.coordMax;
    }

    static getOffsetMin(squareSize) {
        return -parseInt(squareSize / 2.0);
    }

    static getOffsetMax(squareSize) {
        return parseInt(squareSize / 2.0) + (squareSize % 2 == 0 ? -1 : 0);
    }

    /**
     * 
     * @param {number|Array} squareSizes the square sizes to examine
     * @returns position of top-left square
     */
    findMaxPower(squareSizes) {
        if (typeof(squareSizes) === 'number') {
            squareSizes = [squareSizes];
        }
        let cornerPosition = null, maxPower = null;
        squareSizes.forEach(squareSize => {
            console.debug("looking for max power with square size", squareSize);
            const offsetMin = Grid.getOffsetMin(squareSize);
            const offsetMax = Grid.getOffsetMax(squareSize);
            const requiredNumCellsPerSquare = squareSize * squareSize;
            for (let y = this.coordMin; y <= this.coordMax; y++) {
                for (let x = this.coordMin; x <= this.coordMax; x++) {
                    const square = [];
                    let notFull = false;
                    for (let i = offsetMin; !notFull && i <= offsetMax; i++) {
                        for (let j = offsetMin; !notFull && j <= offsetMax; j++) {
                            const xx = x + j, yy = y + i;
                            if (this.contains(xx, yy)) {
                                square.push(new Position(xx, yy));
                            } else {
                                notFull = true;
                            }
                        }
                    }
                    if (notFull) {
                        continue;
                    }
                    if (square.length > requiredNumCellsPerSquare) {
                        throw new Error("bad square size: " + square.length);
                    }
                    if (square.length === requiredNumCellsPerSquare) {
                        const powerSum = square.map(p => FuelCell.findPowerLevel(p.x, p.y, this.serialNumber)).reduce(SUM, 0);
                        if (maxPower === null || powerSum > maxPower) {
                            maxPower = powerSum;
                            cornerPosition = square[0];
                            cornerPosition.squareSize = squareSize;
                        }
                    }
                }
            }
        });
        return cornerPosition;
    }

}

export default {
    FuelCell: FuelCell,
};
