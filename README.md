EMF2014 Power stuff

Files
=====

* nodes.json - nodes in the network
* links.json - links (cables)
* def_node.json - definitions of distros etc
* def_link.json - definitions of links

Requirements
============
python needs networkx and decorator
```
pip install networkx decorator
```

If you want to go stright to pdf you also need Ghostscript-9.19
macOS can get it from http://pages.uoregon.edu/koch/

Generate
========
Straight to pdf
```
./diagram.py | unflatten -l 3  | dot -Tps2 | ps2pdf - > power.pdf
```

or on Mac, preview can convert ps to pdf, with out the need to install ghostscript
```
./diagram.py | unflatten -l 3  | dot -Tps2 > power.ps
```
