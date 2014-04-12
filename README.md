EMF2014 Power stuff

Files
=====

mynet.tt - the actual network
defs.tt - definition of distros etc
power.tt - the actual guts

Generate
========
```
tpage power.tt | dot -T ps2 | ps2pdf - power.pdf
```
