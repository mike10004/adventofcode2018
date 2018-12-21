import fs from 'fs';
import { Grid } from './chronalcharge.mjs';

function main(args) {
    const serialNumber = parseInt(args[0]);
    if (isNaN(serialNumber)) {
        console.error("usage: grid serial number is required as argument");
        return 1;
    }
    const coordMin = 1, coordMax = 300;
    const maxSquareSize = coordMax;
    const grid = new Grid(coordMin, coordMax, serialNumber, true);
    console.debug("finding max power for grid " + grid.toString());
    const corner = grid.findMaxPower(maxSquareSize);
    if (!corner) {
        process.stderr.write("no max power found; 0 cells?\n");
        return 1;
    }
    process.stdout.write("max power is in cell with top-left corner " + corner + " with square size " + corner.squareSize + "\n");
    return 0;
}

process.exitCode = main(process.argv.slice(2));
