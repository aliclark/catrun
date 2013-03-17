
var spawn = require('child_process').spawn;
var ch = null;

var noend = {end: false};

var spawn_prog;
var spawn_args;
var stdin;
var stdout;
var stderr;
var hasunpipe;

function resume() {
    if (ch === null) {
        ch = spawn(spawn_prog, spawn_args);
        ch.stdout.pipe(stdout, noend);
        ch.stderr.pipe(stderr, noend);
        // we will call end() manually
        stdin.pipe(ch.stdin, noend);
        stdin.resume();
    }
}

function heartbeat() {
    // this is only needed so "something" is happening while we wait
    // for a resume signal, otherwise the program would just quit.
}

function pause() {
    if (ch !== null) {
        stdin.pause();

        if (hasunpipe) {
            stdin.unpipe(ch.stdin);
        }
        ch.stdin.end();
        ch = null;
        // hopefully now the old ch will die normally
    }
}

function end() {
    pause();
    // is there a need/way to wait on the child pid?
    process.exit();
}

function main() {
    spawn_prog = process.argv[2];
    spawn_args = process.argv.slice(3);
    stdin = process.stdin;
    stdout = process.stdout;
    stderr = process.stderr;
    hasunpipe = (typeof stdin.unpipe) === 'function';

    stdin.on('end', end);
    process.on('SIGUSR1', resume);
    process.on('SIGUSR2', pause);
    resume();

    setInterval(heartbeat, 1000);
}

main();
