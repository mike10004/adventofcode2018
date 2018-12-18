import {describe, it} from '../common/exams/lib/exams';
import assert from 'assert';
import { Node, Parser } from './navtree';

function getSampleNodeList() {
    const parser = Parser.fromText("2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2");
    return parser.consumeAll();
}

describe("Parser", () => {

    it("consumeAll", () => {
        const parser = Parser.fromText("2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2");
        const nodes = parser.consumeAll();
        assert.equal(nodes.length, 4);
    });
    
});

describe("Node", () => {

    it("sumMetadatas", () => {
        const nodes = getSampleNodeList();
        let metadataSum = 0;
        nodes.forEach(node => {
            // process.stderr.write("\n\n");
            // process.stderr.write(node.toString());
            // process.stderr.write("\n\n");
            // console.log(node.metadatas);
            metadataSum += node.sumMetadatas();
        });
        assert.equal(metadataSum, 138);
        const root = Node.findRoot(nodes);
        assert.notEqual(typeof(root), 'undefined');
        assert.equal(root.sumMetadatas(true), 138);
    });

    it("value", () => {
        const nodes = getSampleNodeList();
        const root = Node.findRoot(nodes);
        assert.notEqual(typeof(root), 'undefined');
        assert.equal(root.value(), 66);
    });

});