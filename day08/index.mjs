import fs from 'fs';
// import {Bar} from './foo';

function main(args) {
    const pathname = args[0];
    if (!pathname) {
        console.error("usage: pathname of input file is required as argument");
        return 1;
    }
    const text = fs.readFileSync(pathname, {encoding: 'utf8'});
    // ...
    return 0;
}

process.exitCode = main(process.argv.slice(2));
