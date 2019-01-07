import {Elf, Scoreboard, RecipeMachine} from './chocolate';
import 'process';

console.debug("argv", process.argv);
const input = process.argv[2] || '637061';
const iterations = parseInt(process.argv[3] || '10');
const scoreboard = Scoreboard.create(input);
const elves = Elf.createArray(2);
const machine = new RecipeMachine(scoreboard);

for (let i = 0; i < iterations; i++) {
    machine.combine(elves);
    process.stdout.write(scoreboard.render(elves));
    process.stdout.write("\n");
}

const answer = scoreboard.substring(input.length, iterations);
process.stdout.write(answer + "\n");