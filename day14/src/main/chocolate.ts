
const markersTable = [
    "()",
    "[]",
    "{}",
    "<>",
];

function getMarkers(index : number) : string {
    return markersTable[index % markersTable.length];
}

export class Elf {

    constructor(public current: number, public markers : string) {
    }

    static createArray(length : number) : Array<Elf> {
        const elves = new Array<Elf>();
        for (let i = 0; i < length; i++) {
            elves.push(new Elf(i, getMarkers(i)));
        }
        return elves;
    }
}

function surround(value : any, markers : string) {
    const prefix = markers.substr(0, markers.length / 2);
    const suffix = markers.substr(markers.length / 2, markers.length / 2);
    return prefix + value.toString() + suffix;
}

export class Scoreboard {

    constructor(public cells : Array<number>) {
    }

    cell(index: number) : number {
        return this.cells[index % this.cells.length];
    }

    static create(initialEntries : string) : Scoreboard {
        return new Scoreboard(initialEntries.split('').map(ch => parseInt(ch, 10)));
    }

    length() {
        return this.cells.length;
    }

    append(score : number) {
        this.cells.push(score);
    }

    private renderScore(position : number, elves : Array<Elf>) : string {
        let markers = "  ";
        elves.forEach(elf => {
            if (elf.current === position) {
                markers = elf.markers;
            }
        });
        return surround(this.cell(position), markers);
    }

    render(elves : Array<Elf>) : string {
        return this.cells.map((score, position) => this.renderScore(position, elves)).join('');
    }

    substring(start : number, length : number) : string {
        return this.cells.slice(start, start + length).join('');
    }
}

export class Numbers {

    static getDigits(value : number) : Array<number> {
        // TODO reimplement without string parsing
        return Math.abs(value).toString().split('').map(ch => parseInt(ch, 10));
    }

}

export class Arrays {
    
    static findSequence(cells : Array<any>, sequence : Array<any>, start : number) : number {
        // if (sequence.length === 0) {
        //     return 0;
        // }
        for (let i = start; i <= cells.length - sequence.length; i++) {
            let j = 0;
            for (; j < sequence.length; j++) {
                if (cells[i + j] !== sequence[j]) {
                    break;
                }
            }
            if (j === sequence.length) {
                return i;
            }
        }
        return -1;
    }
        
}

export class RecipeMachine {

    constructor(public scoreboard : Scoreboard) {

    }

    advance(elves : Array<Elf>) {
        elves.forEach(elf => {
            elf.current = (elf.current + 1 + this.scoreboard.cell(elf.current)) % this.scoreboard.length();
        });        
    }

    combine(elves : Array<Elf>) {
        let recipeSum = 0;
        elves.forEach(elf => {
            recipeSum += this.scoreboard.cell(elf.current);
        });
        Numbers.getDigits(recipeSum).forEach(digit => {
            this.scoreboard.append(digit);
        });
        this.advance(elves);
    }

}