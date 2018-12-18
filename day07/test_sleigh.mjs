import {describe, it} from '../common/exams/lib/exams';
import assert from 'assert';
import { ArrayUtils, Step, Sequencer } from './sleigh';

describe("ArrayUtils", () => {
    it("contains", () => {
        assert.equal(ArrayUtils.contains([1, 2, 3], 2), true);
    });
});

const SAMPLE_TEXT = "Step C must be finished before step A can begin.\n" + 
"Step C must be finished before step F can begin.\n" + 
"Step A must be finished before step B can begin.\n" + 
"Step A must be finished before step D can begin.\n" + 
"Step B must be finished before step E can begin.\n" + 
"Step D must be finished before step E can begin.\n" + 
"Step F must be finished before step E can begin.\n";

describe("Step", () => {

    it("parseAll", () => {
        const text = SAMPLE_TEXT;
        const steps = Step.parseAll(text);
        assert.equal("ABCDEF".length, Object.keys(steps).length);
        Object.values(steps).forEach(step => {
            assert.notEqual(typeof(step.id), "undefined"); 
        })
    });

});

describe("Sequencer", () => {
    it("compute", () => {
        const steps = Step.parseAll(SAMPLE_TEXT);
        const sequence = new Sequencer().compute(steps);
        assert.deepEqual(sequence, ['C', 'A', 'B', 'D', 'F', 'E']);
    });
});