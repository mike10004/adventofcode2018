
export class ArrayUtils {

    static contains(haystack, needle) {
        return haystack.indexOf(needle) >= 0;
    }

}

export class Step {
    
    constructor(id) {
        this.id = id;
        this.dependencies = new Set();
    }

    addDependency(stepId) {
        this.dependencies.add(stepId);
    }

    /**
     * 
     * @param {Set} completed set of completed step IDs
     */
    isDoable(completed) {
        for (let dep of this.dependencies) {
            if (!completed.has(dep)) {
                return false;
            }
        }
        return true;
    }

    static parseAll(text) {
        const steps = {};
        for (let line of text.split("\n")) {
            if (line) {
                const m = /^Step (\w+) must be finished before step (\w+) can begin/.exec(line);
                if (m) {
                    const id = m[2];
                    const dep = m[1];
                    let step = steps[id];
                    if (!step) {
                        step = new Step(id);
                        steps[id] = step;
                    }
                    step.addDependency(dep);
                    if (!(dep in steps)) {
                        steps[dep] = new Step(dep);
                    }
                } else {
                    console.info("does not match expected pattern", line);
                }
            }
        }
        return steps;
    }

}

export class Sequencer {

    /**
     * 
     * @param {object} steps an object whose keys are step IDs and whose values are Step objects
     */
    compute(steps) {
        const numSteps = Object.keys(steps).length;
        const completed = new Set();
        const sequence = [];
        while (sequence.length < numSteps) {
            const doable = this.findDoable(steps, completed);
            if (doable.length === 0) {
                console.info("not doable");
                return null;
            }
            const id = doable[0];
            sequence.push(id);
            completed.add(id);
        }
        return sequence;
    }

    findDoable(steps, completed) {
        const doable = [];
        for (let id in steps) {
            if (!completed.has(id)) {
                const step = steps[id];
                if (step.isDoable(completed)) {
                    doable.push(id);
                }
            }
        }
        doable.sort();
        return doable;
    }

}

export default Sequencer;
