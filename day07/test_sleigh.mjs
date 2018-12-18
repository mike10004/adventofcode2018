import {describe, it} from '../common/exams/lib/exams';
import assert from 'assert';
import { ArrayUtils, Step, Sequencer, Builder, Scheduler } from './sleigh';

const SAMPLE_TEXT = "Step C must be finished before step A can begin.\n" + 
"Step C must be finished before step F can begin.\n" + 
"Step A must be finished before step B can begin.\n" + 
"Step A must be finished before step D can begin.\n" + 
"Step B must be finished before step E can begin.\n" + 
"Step D must be finished before step E can begin.\n" + 
"Step F must be finished before step E can begin.\n";

describe("ArrayUtils", () => {
    it("contains", () => {
        assert.equal(ArrayUtils.contains([1, 2, 3], 2), true);
    });
    it("does not contain", () => {
        assert.equal(ArrayUtils.contains([-4, 6, 100], 37), false);
    });
});

describe("Step", () => {

    it("parseAll", () => {
        const text = SAMPLE_TEXT;
        const steps = Step.parseAll(text);
        assert.equal("ABCDEF".length, Object.keys(steps).length);
        Object.values(steps).forEach(step => {
            assert.notEqual(typeof(step.id), "undefined"); 
        });
    });

});

describe("Sequencer", () => {
    it("compute", () => {
        const steps = Step.parseAll(SAMPLE_TEXT);
        const sequence = new Sequencer().compute(steps);
        assert.deepEqual(sequence.join(''), 'CABDFE');
    });
});

describe("Scheduler", () => {
    it("compute", () => {
        const steps = Step.parseAll(SAMPLE_TEXT);
        const workers = [new Builder(), new Builder()];
        const scheduler = new Scheduler(workers, 0);
        const listener = (_, steps, completed) => {
            console.debug(scheduler.second, scheduler.state().join(''), Array.from(completed).join(''));
        }
        scheduler.proceed(steps, listener, 100);
        assert.equal(scheduler.second, 15);
    });
});
