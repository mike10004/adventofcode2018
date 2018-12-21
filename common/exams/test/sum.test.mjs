import {describe, it, xdescribe, xit} from '../lib/exams';
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
    xit("ignored test inside not-ignored block", () => {
        assert.fail("should never run");
    });
    it("add negative numbers", () => {
        assert.equal(sum(-5, -6), -11);
    });
});

xdescribe("ignored group", () => {
    it("an ignored test", () => {
        assert.fail("should never run");
    });
});

it("sub anon", () => {
    assert.equal(true, true);
});

xit("sub anon 2 ignored", () => {
    assert.fail("should be ignored");
});