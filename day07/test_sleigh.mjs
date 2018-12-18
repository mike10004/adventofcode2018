import {describe, it} from '../common/exams/lib/exams';
import assert from 'assert';
import { ArrayUtils, Step, Sequencer } from './sleigh';

describe("ArrayUtils", function() {
    it("contains", function() {
        assert.equal(ArrayUtils.contains([1, 2, 3], 2), true);
    });
});
