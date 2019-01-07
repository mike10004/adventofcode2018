import { expect } from 'chai';
import { Numbers, Elf, Scoreboard, RecipeMachine } from '../main/chocolate';

describe('Numbers', () => {

    it('getDigits', () => {
        expect(Numbers.getDigits(10)).to.deep.equal([1, 0]);
    });

});

describe('Scoreboard', () => {
    it('create', () => {
        const scoreboard = Scoreboard.create('637061');
        expect(scoreboard.cells).to.deep.equal([6, 3, 7, 0, 6, 1]);
    });
})

describe('RecipeMachine', () => {

    it('combine', () => {
        const scoreboard = new Scoreboard([3, 7]);
        const machine = new RecipeMachine(scoreboard);
        const elves = Elf.createArray(2);
        machine.combine(elves);
        expect(scoreboard.cells).to.deep.equal([3, 7, 1, 0]);
    });

    [
        {after: 9, expected: '5158916779'},
        {after: 5, expected: '0124515891'},
        {after: 18, expected: '9251071085'},
        {after: 2018, expected: '5941429882'},
    ].forEach(testCase => {
        it('many iterations: ' + JSON.stringify(testCase), () => {
            const scoreboard = new Scoreboard([3, 7]);
            const machine = new RecipeMachine(scoreboard);
            const elves = Elf.createArray(2);
            // console.debug(scoreboard.render(elves));
            for (let i = 0; i < testCase.after + testCase.expected.length; i++) {
                machine.combine(elves);
                // console.debug(scoreboard.render(elves));
            }
            const actual = scoreboard.substring(testCase.after, testCase.expected.length);
            expect(actual).to.equal(testCase.expected);
        });
    })

});
