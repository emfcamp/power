#!/opt/local/bin/python
import json
import networkx as nx
import matplotlib.pyplot as plt

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

G = nx.DiGraph()
G.add_nodes_from(nodes)

for l in links:
	G.add_edge(l['src'],l['dst'], length=l['length'])

print G.nodes()
print G.edges()


nx.draw (G)
plt.draw()
plt.show()


