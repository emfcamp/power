EMF2014 Power stuff

Files
=====

* nodes.json - nodes in the network
* links.json - links (cables)
* def_node.json - definitions of distros etc
* def_link.json - definitions of links

Generate
========
```
./diagram.py | unflatten -l 3  | dot -Tps2 | ps2pdf - > power.pdf
```
