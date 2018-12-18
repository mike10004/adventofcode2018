
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

    isDoable(completed) {
        for (let dep of this.dependencies) {
            if (!ArrayUtils.contains(completed, dep)) {
                return false;
            }
        }
        return true;
    }

}

export class Sequencer {

    compute(steps) {
        throw new Error("not yet implemented");
    }

}

export default Sequencer;
