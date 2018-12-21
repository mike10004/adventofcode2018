import fs from 'fs';
import { Grid } from './chronalcharge.mjs';

function main(args) {
    const serialNumber = parseInt(args[0]);
    if (isNaN(serialNumber)) {
        console.error("usage: grid serial number is required as argument");
        return 1;
    }
    const coordMin = 1, coordMax = 300;
    const squareSizes = [];
    for (let q = coordMin; q <= coordMax; q++) {
        squareSizes.push(q);
    }
    const grid = new Grid(coordMin, coordMax, serialNumber);
    console.debug("finding max power for grid " + grid.toString());
    const corner = grid.findMaxPower(squareSizes);
    process.stdout.write("max power is in cell with top-left corner " + corner + " with square size " + corner.squareSize + "\n");
    return 0;
}

process.exitCode = main(process.argv.slice(2));
