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

class Cache {
    
    constructor(size, loader) {
        this.size = size;
        this.map = new Map();
        this.loader = loader;
    }

    get(key) {
        if (typeof(key) !== 'string') {
            key = key.toString();
        }
        let value = this.map.get(key);
        if (typeof(value) === 'undefined') {
            while (this.map.size >= size) {
                const oldestKey = this.map.keys().next();
                this.map.delete(oldestKey);
            }
            value = this.loader(key);
            this.map.put(key, value);
        }
        return value;
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

    /**
     * 
     * @param {number} squareSize the square size
     * @returns position of top-left square
     */
    findMaxPower(squareSize) {
        const cache = new Cache();
        let cornerPosition = null, maxPower = null;
        const offsetMin = -parseInt(squareSize / 2.0);
        const offsetMax = -offsetMin;
        const requiredNumCellsPerSquare = squareSize * squareSize;
        for (let y = this.coordMin; y <= this.coordMax; y++) {
            for (let x = this.coordMin; x <= this.coordMax; x++) {
                const square = [];
                for (let i = offsetMin; i <= offsetMax; i++) {
                    for (let j = offsetMin; j <= offsetMax; j++) {
                        const xx = x + j, yy = y + i;
                        if (this.contains(xx, yy)) {
                            square.push(new Position(xx, yy));
                        }
                    }
                }
                if (square.length > requiredNumCellsPerSquare) {
                    throw new Error("bad square size: " + square.length);
                }
                if (square.length === requiredNumCellsPerSquare) {
                    const powerSum = square.map(p => FuelCell.findPowerLevel(p.x, p.y, this.serialNumber)).reduce(SUM, 0);
                    if (maxPower === null || powerSum > maxPower) {
                        maxPower = powerSum;
                        cornerPosition = square[0];
                    }
                }
            }
        }
        return cornerPosition;
    }

}

export default {
    FuelCell: FuelCell,
};
