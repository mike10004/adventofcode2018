import {describe, it} from '../common/exams/lib/exams';
import assert from 'assert';
import { Parser } from './navtree';

describe("Parser", () => {
    it("consumeAll", () => {
        const parser = Parser.fromText("2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2");
        const nodes = parser.consumeAll();
        assert.equal(nodes.length, 4);
        let metadataSum = 0;
        nodes.forEach(node => {
            // process.stderr.write("\n\n");
            // process.stderr.write(node.toString());
            // process.stderr.write("\n\n");
            // console.log(node.metadatas);
            metadataSum += node.sumMetadatas();
        });
        assert.equal(metadataSum, 138);
        const root = nodes.filter(n => !n.hasParent)[0];
        assert.notEqual(typeof(root), 'undefined');
        assert.equal(root.sumMetadatasRecursively(), 138);
    });
});

