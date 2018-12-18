/*
 * module navtree
 */

const SUM = (a, b) => a + b;

export class Node {
    
    constructor(children, metadatas, hasParent) {
        this.children = children;
        this.metadatas = metadatas;
        this.hasParent = hasParent;
    }

    sumMetadatas() {
        return this.metadatas.reduce(SUM, 0);
    }

    sumMetadatasRecursively() {
        return this.sumMetadatas() + this.children.map(n => n.sumMetadatasRecursively()).reduce(SUM, 0);
    }

    toString() {
        return JSON.stringify(this, null, 2);
    }

    isLeaf() {
        return this.children.length === 0;
    }
}

export class Parser {

    constructor(values) {
        this.values = values;
        this.pos = 0;
    }

    static fromText(text) {
        const values = text.split(/\s+/).map(t => parseInt(t, 10));
        return new Parser(values);
    }

    consumeAll() {
        const nodes = [];
        this.consumeNode(nodes, false);
        return nodes;
    }

    consumeNode(nodes, hasParent) {
        const numChildren = this.values[this.pos];
        this.pos++;
        const numMetadatas = this.values[this.pos];
        this.pos++;
        const children = [];
        for (let i = 0; i < numChildren; i++) {
            const child = this.consumeNode(nodes, true);
            children.push(child);
        }
        const metadatas = [];
        for (let i = 0; i < numMetadatas; i++) {
            metadatas.push(this.values[this.pos]);
            this.pos++;
        }
        const node = new Node(children, metadatas, hasParent);
        nodes.push(node);
        return node;
    }
}

export default {
    'Parser': Parser
};
