
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

    /**
     * 
     * @param steps 
     * @param completed 
     * @param {function|undefined} filter predicate satisfied only by IDs of allowable steps
     */
    findDoable(steps, completed, filter) {
        filter = filter || (x => true);
        const doable = [];
        for (let id in steps) {
            if (!completed.has(id) && filter(id)) {
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

export class Task {
    
    constructor(id, duration, startTime) {
        this.id = id;
        this.duration = duration;
        this.startTime = startTime;
    }

    isCompleted(currentTime) {
        return currentTime >= (this.startTime + this.duration);
    }

    static start(id, floor, currentTime) {
        const duration = floor + " ABCDEFGHIJKLMNOPQRSTUVWXYZ".indexOf(id);
        return new Task(id, duration, currentTime);
    }
}

export class Builder {

    constructor() {
        this.task = null;
    }

    assign(task) {
        this.task = task;
    }

    isIdle() {
        return !this.task;
    }

    clear() {
        this.task = null;
    }

    currentTaskId() {
        return !!this.task ? this.task.id : ".";
    }
}

export class Scheduler {

    constructor(workers, floor) {
        this.sequencer = new Sequencer();
        this.second = -1;
        this.floor = floor || 0;
        this.workers = workers || ([new Builder()]);
    }

    /**
     * 
     * @param {Set} completed set of IDs of completed tasks
     */
    tick(steps, completed) {
        this.second++;
        const stepsInProgress = new Set();
        this.workers.forEach(worker => {
            if (!worker.isIdle()) {
                if (worker.task.isCompleted(this.second)) {
                    completed.add(worker.task.id);
                    worker.clear();
                } else {
                    stepsInProgress.add(worker.task.id);
                }
            }
        });
        const idleWorkers = this.workers.filter(w => w.isIdle());
        if (idleWorkers.length > 0) {
            const notInProgress = id => !stepsInProgress.has(id);
            const doable = this.sequencer.findDoable(steps, completed, notInProgress)
            if (doable.length > 0) {
                for (let i = 0; i < Math.min(doable.length, idleWorkers.length); i++) {
                    const step = doable[i];
                    const worker = idleWorkers[i];
                    worker.assign(Task.start(step, this.floor, this.second));
                }
            }
        }
    }

    proceed(steps, listener, maxTotalDuration) {
        listener = listener || (() => {});
        const completed = new Set();
        const numSteps = Object.keys(steps).length;
        while (completed.size < numSteps) {
            this.tick(steps, completed);
            listener(this, steps, completed);
            if (this.second > maxTotalDuration) {
                console.warn("break early due to max duration elapsed", maxTotalDuration);
                break;
            }
        }
        return this.second;
    }

    state() {
        return this.workers.map(w => w.currentTaskId());
    }
}

export default {
    Sequencer: Sequencer,
    ArrayUtils: ArrayUtils,
    Step: Step,
    Builder: Builder,
    Scheduler: Scheduler,
    Task: Task,
};
