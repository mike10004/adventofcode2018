import fs from 'fs';
import {Node, Parser} from './navtree';

function main(args) {
    const pathname = args[0];
    if (!pathname) {
        console.error("usage: pathname of input file is required as argument");
        return 1;
    }
    const text = fs.readFileSync(pathname, {encoding: 'utf8'});
    const parser = Parser.fromText(text);
    const nodes = parser.consumeAll();
    const root = Node.findRoot(nodes);
    const metadataSum = root.sumMetadatas(true);
    process.stdout.write("metadata sum " + metadataSum + "\n");
    const rootValue = root.value();
    process.stdout.write("root value " + rootValue + "\n");
    return 0;
}

process.exitCode = main(process.argv.slice(2));
