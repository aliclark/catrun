catrun
======

cat data into a child process, stopping and restarting the child at any point

This can be used to change the functionality of a long-lived pipe without
breaking the pipe itself.

Instead of perhaps the following:

```sh
tailf datafile | grep ... | awk ... >>outfile
```

```sh
tailf datafile | node catrun.js mypipe >>outfile
```

where the program "mypipe" performs 'grep ... | awk ...'

The benefit is that if a few hours into the execution of the program you wish
to change eg. the value being grep'd, then all that's needed is to edit the
mypipe script, kill -USR2 the catrun process, and kill -USR1 to start it again.

If you have a stateful program as part of the pipe, simply make sure the
program saves its state before terminating, and loads its state before
starting, and the program can be freely restarted using catrun.

