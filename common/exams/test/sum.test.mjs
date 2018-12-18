import {describe, it} from '../lib/exams';
import assert from 'assert';
import sum from './sum';

describe("summing", () => {
    it("add positive numbers", () => {
        assert.equal(sum(1, 2), 3);
    });
    it("fail an assertion", () => {
        assert.equal(false, true);
    });
    it("emit an error", () => {
        throw new Error("this is an error");
    });
    it("add negative numbers", () => {
        assert.equal(sum(-5, -6), -11);
    });
});

it("sub anon", () => {
    assert.equal(true, true);
});
