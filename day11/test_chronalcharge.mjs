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

    [
        {squareSize: 1, expectedMin: 0, expectedMax: 0},
        {squareSize: 2, expectedMin: -1, expectedMax: 0},
        {squareSize: 3, expectedMin: -1, expectedMax: 1},
        {squareSize: 4, expectedMin: -2, expectedMax: 1},
        {squareSize: 5, expectedMin: -2, expectedMax: 2},
        {squareSize: 7, expectedMin: -3, expectedMax: 3},
    ].forEach(testCase => {
        it("getOffsetMin at size " + testCase.squareSize, () => {
            assert.equal(Grid.getOffsetMin(testCase.squareSize), testCase.expectedMin);
        });
        it("getOffsetMax at size " + testCase.squareSize, () => {
            assert.equal(Grid.getOffsetMax(testCase.squareSize), testCase.expectedMax);
        });
    });

    it("example 1", () => {
        const actual = new Grid(1, 300, 18).findMaxPower(3);
        assert.notEqual(actual, null);
        assert.equal(actual.toString(), "33,45");
    });

    it("example 2", () => {
        const actual = new Grid(1, 300, 42).findMaxPower(3);
        assert.notEqual(actual, null);
        assert.equal(actual.toString(), "21,61");
    });

});