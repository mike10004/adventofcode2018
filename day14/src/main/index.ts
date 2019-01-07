import {Elf, Scoreboard, RecipeMachine} from './chocolate';
import 'process';

console.debug("argv", process.argv);
const goodThreshold = parseInt(process.argv[2] || '637061', 10);
const numSubsequent = parseInt(process.argv[3] || '10', 10);
const iterations = goodThreshold + numSubsequent;
const scoreboard = new Scoreboard([3, 7]);
const elves = Elf.createArray(scoreboard.length());
const machine = new RecipeMachine(scoreboard);

for (let i = 0; i < iterations; i++) {
    machine.combine(elves);
    // process.stdout.write(scoreboard.render(elves));
    // process.stdout.write("\n");
}

const answer = scoreboard.substring(goodThreshold, numSubsequent);
process.stdout.write(answer + "\n");