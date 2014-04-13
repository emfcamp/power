#!/usr/bin/python
import json

f1 = open ('nodes.json')
f2 = open ('links.json')
f3 = open ('def_node.json')
f4 = open ('def_link.json')

nodes=json.load(f1)
links=json.load(f2)
def_node=json.load(f3)
def_link=json.load(f4)

f1.close()
f2.close()
f3.close()
f4.close()

print nodes, links, def_node, def_link

print def_link

