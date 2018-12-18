import fs from 'fs';
import {Sequencer, Step} from './sleigh';

function main(args) {
    const pathname = args[0];
    if (!pathname) {
        console.error("usage: pathname of input file is required as argument");
        return 1;
    }
    const text = fs.readFileSync(pathname, {encoding: 'utf8'});
    const steps = Step.parseAll(text);
    const numSteps = Object.keys(steps).length;
    process.stderr.write(numSteps + " steps parsed from input\n");
    if (numSteps === 0) {
        console.error("no steps parsed from input", args);
        return 1;
    }
    const sequencer = new Sequencer();
    const sequence = sequencer.compute(steps);
    if (!sequence || sequence.length === 0) {
        console.error("sequencer returned falsey value", sequence);
        return 2;
    }
    process.stdout.write(sequence.join(''));
    process.stdout.write("\n");
    return 0;
}

process.exitCode = main(process.argv.slice(2));
