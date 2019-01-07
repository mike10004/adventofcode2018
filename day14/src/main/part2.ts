import {Elf, Scoreboard, RecipeMachine, Arrays} from './chocolate';
import 'process';

const puzzleInput = process.argv[2] || '637061';
const scoreboard = new Scoreboard([3, 7]);
const query = puzzleInput.split('').map(ch => parseInt(ch, 10));
const elves = Elf.createArray(scoreboard.length());
const machine = new RecipeMachine(scoreboard);
const maxIterations = 100000000;
let index = -1, searchStart = 0;

for (let numIterations = 0; index < 0; numIterations++) {
    index = Arrays.findSequence(scoreboard.cells, query, searchStart);
    searchStart = Math.max(0, scoreboard.cells.length - query.length);
    machine.combine(elves);
    if (numIterations > maxIterations) {
        process.stderr.write("reached max iterations\n");
        break;
    }
}

if (index >= 0) {
    process.stdout.write(index.toString());
    process.stdout.write(" recipes appear before ");
    process.stdout.write(puzzleInput);
    process.stdout.write("\n");
}
