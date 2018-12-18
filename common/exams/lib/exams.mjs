import {AssertionError} from 'assert';

const _PASS = 'pass';
const _FAIL = 'fail';
const _ERROR = 'error';

class Result {
    
    constructor(test, outcome, extras) {
        this.test = test;
        this.outcome = outcome;
        this.extras = extras;
    }

}

class Renderer {

    constructor(output) {
        this.output = output;
    }

    stringify(thing, hint) {
        if (thing) {
            if (thing instanceof Test || thing instanceof TestGroup) {
                return thing.description;
            }
            if (hint === 'outcome' && thing !== _PASS) {
                return thing.toString().toUpperCase();
            }
            return thing.toString();
        } else {
            if (hint && hint !== 'extras') {
                return "empty " + hint;
            }
            return "";
        }
    }

    render(thing, hint) {
        const s = this.stringify(thing, hint);
        this.output.write(s);
        return this;
    }

    break() {
        this.output.write("\n");
        return this;
    }

    tab() {
        this.output.write("\t");
        return this;
    }

}

class Summary {

    constructor(numTests, numFailures, numErrors) {
        this.numTests = numTests;
        this.numFailures = numFailures;
        this.numErrors = numErrors;
    }

    static analyze(results) {
        const numTests = results.length;
        const numErrors = results.filter(r => r.outcome === _ERROR).length;
        const numFailures = results.filter(r => r.outcome === _ERROR).length;
        return new Summary(numTests, numFailures, numErrors);
    }

    didAllPass() {
        return this.numErrors === 0 && this.numFailures === 0;
    }

    isEmpty() {
        return this.numTests === 0;
    }

    describe() {
        return this.numTests + " tests executed; " + this.numFailures + " failures, " + this.numErrors + " errors";
    }
}

class Reporter {

    constructor(renderer) {
        this.renderer = renderer;
    }

    groupStarted(group) {
        this.renderer.render(group).break();
    }

    groupFinished(group) {
        this.renderer.break();
    }

    testStarted(test) {
        // no op
    }

    testFinished(result) {
        this.renderer.tab()
            .render(result.outcome, 'outcome').tab()
            .render(result.test, 'test').tab()
            .break();
    }

    allTestsFinished(results) {
        results.forEach(result => {
            if (result.outcome !== _PASS) {
                this.renderer.render(result.test.group);
                this.renderer.output.write(" - ");
                this.renderer.render(result.test);
                this.renderer.break();
                if (result.extras instanceof Error) {
                    const ex = result.extras;
                    if (ex instanceof AssertionError) {
                        this.renderer.render(ex.toString()).break();
                        if (ex.stack) {
                            this.renderer.render(ex.stack.split("\n").slice(1, 2)).break();
                        }
                    } else if (ex.stack) {
                        this.renderer.render(ex.stack, "stacktrace");
                    } else {
                        this.renderer.render(ex).break();
                    }
                }
                this.renderer.break();
            }
        });
    }

}

class Runner {

    constructor() {
    }

    execute(state, reporter) {
        state.executed = true;
        const results = [];
        state.groups.forEach(group => {
            reporter.groupStarted(group);
            group.tests.forEach(test => {
                let outcome = _ERROR, extras = null;
                try {
                    reporter.testStarted(test);
                    test.run();
                    outcome = _PASS;
                } catch (e) {
                    extras = e;
                    if (e instanceof AssertionError) {
                        outcome = _FAIL;
                    } else {
                        outcome = _ERROR;
                    }                    
                }
                const result = new Result(test, outcome, extras);
                reporter.testFinished(result);
                results.push(result);
            });
            reporter.groupFinished(group);
        });
        reporter.allTestsFinished(results);
        return results;
    }

}

class State {

    constructor() {
        this.groups = [];
        this.currentGroup = null;
        this.executed = false;
    }
    
    addGroup(group) {
        this.groups.push(group);
        this.currentGroup = group;
    }

    getCurrentGroup() {
        if (!this.currentGroup) {
            this.addGroup(new TestGroup("anonymous " + this.groups.length));
        }
        return this.currentGroup;
    }

    clearCurrentGroup() {
        this.currentGroup = null;
        return this;
    }

    isExecuted() {
        return this.executed;
    }
}

const global = new State();

function getState() {
    return global;
}

class TestGroup {
    
    constructor(description) {
        this.description = description;
        this.tests = [];
    }

    it(description, fn) {
        return this.addTest(new Test(this, description, fn));
    }
    
    addTest(test) {
        this.tests.push(test);
        return this;
    }
}

class Test {

    constructor(group, description, fn) {
        this.group = group;
        this.description = description;
        this.fn = fn;
    }

    run() {
        return this.fn();
    }

}

export function describe(description, runNow) {
    const group = new TestGroup(description);
    const state = getState();
    state.addGroup(group);
    if (runNow) {
        runNow();
        state.clearCurrentGroup();
    }
    return group;
};

export function it(description, runnable) {
    getState().getCurrentGroup().it(description, runnable);
};

export function execute() {
    const renderer = new Renderer(process.stdout);
    const reporter = new Reporter(renderer);
    const runner = new Runner();
    const state = getState();
    const results = runner.execute(state, reporter);
    const summary = Summary.analyze(results);
    renderer.render(summary.describe() + "\n");
    let exitCode = 0;
    if (summary.isEmpty()) {
        process.stderr.write("no tests executed\n");
        exitCode = 1;
    } else if (!summary.didAllPass()) {
        exitCode = 2;
    }
    return exitCode;
}

const exams = {
    describe: describe,
    execute: execute,
    it: it,
    version: 1
};

export default exams;

(function addShutdownHook(){
    process.on('beforeExit', () => {
        const state = getState();
        if (!state.isExecuted()) {
            process.exitCode = execute();
        }
    });
})();
