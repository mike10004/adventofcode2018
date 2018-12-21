import {describe, it, xdescribe, xit} from '../common/exams/lib/exams';
import assert from 'assert';
import { Position, FuelCell } from './chronalcharge';
import { Grid } from './chronalcharge.mjs';

describe("FuelCell", () => {
    
    it("getHundredsDigit", () => {
        assert.equal(FuelCell.getHundredsDigit(1234), 2);
    });
    it("getHundredsDigit", () => {
        assert.equal(FuelCell.getHundredsDigit(57), 0);
    });
    it("getHundredsDigit", () => {
        assert.equal(FuelCell.getHundredsDigit(1000000), 0);
    });
    it("getHundredsDigit", () => {
        assert.equal(FuelCell.getHundredsDigit(9999), 9);
    });
   
    [
        [122, 79, 57, -5],
        [217, 196, 39, 0],
        [101, 153, 71, 4],
    ].forEach(testCase => {
        it("findPowerLevel", () => {
            const x = testCase[0], y = testCase[1];
            const serialNumber = testCase[2], expected = testCase[3];
            const actual = FuelCell.findPowerLevel(x, y, serialNumber);
            assert.equal(actual, expected);
        });
    })

});

describe("Grid", () => {

    it("trivial", () => {
        const actual = new Grid(1, 300, 18).findMaxPower(1, 3);
        assert.notEqual(actual, null);
        console.debug("result", actual);
    });

    it("example 1", () => {
        const actual = new Grid(1, 300, 18).findMaxPower(3);
        assert.notEqual(actual, null);
        assert.equal(actual.toString(), "33,45");
        assert.equal(actual.squareSize, 3);
    });

    it("example 2", () => {
        const actual = new Grid(1, 300, 42).findMaxPower(3);
        assert.notEqual(actual, null);
        assert.equal(actual.toString(), "21,61");
        assert.equal(actual.squareSize, 3);
    });

    it("example 3", () => {
        const actual = new Grid(1, 300, 18).findMaxPower(24);
        assert.notEqual(actual, null);
        assert.equal(actual.toString(), "90,269");
        assert.equal(actual.squareSize, 16);
    });

    it("example 4", () => {
        const actual = new Grid(1, 300, 42).findMaxPower(20);
        assert.notEqual(actual, null);
        assert.equal(actual.toString(), "232,251");
        assert.equal(actual.squareSize, 12);
    });

});