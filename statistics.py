#!/usr/bin/env python
import json
import networkx as nx
import matplotlib.pyplot as plt
import operator
from collections import Counter

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

G = nx.Graph()
G.add_nodes_from(nodes)

for l in links:
	l_type = def_node[nodes[l['dst']]]['in']
	vDrop = def_link[l_type]['mvperM'] * l['length']
	mass = def_link[l_type]['density'] * l['length']
	G.add_edge(l['src'],l['dst'], length=l['length'], vDrop=vDrop, mass=mass, ltype=l_type)


SG={}
gens = {k for (k,v) in nodes.items() if v =='gen'}
for gen in gens:
	SG[gen] = G.subgraph( nx.node_connected_component(G,gen) )

print
print "Grid\tNodeCt\tCableCt\tCableLeng[m]\tCableMass[kg]"
for gen in gens:
	print gen, 
	print "\t",nx.number_of_nodes(SG[gen]),
	print "\t",nx.number_of_edges(SG[gen]),
	print "\t", sum(nx.get_edge_attributes(SG[gen],'length').values()),
	print "\t", sum(nx.get_edge_attributes(SG[gen],'mass').values())
print "Total\t", 
print nx.number_of_nodes(G),
print "\t",nx.number_of_edges(G),
print "\t", sum(nx.get_edge_attributes(G,'length').values()),
print "\t", sum(nx.get_edge_attributes(G,'mass').values())
 
ltypes=def_link.keys()
count = dict.fromkeys(ltypes,0)
tlength = dict.fromkeys(ltypes,0)

for (x,y,e) in G.edges(data=True):
	count[e['ltype']]+=1
	tlength[e['ltype']]+=e['length']


print
#print "LType\t\tCount\tLength"
#for l in def_link.keys():
#	print l,'\t\t',count[l],'\t',tlength[l]
#print count
#print tlength

nodedist={}
nodevDrop={}
nodeGrid={}

for gen in gens:
	for n in SG[gen].nodes():
		nodedist[n] = nx.shortest_path_length(SG[gen],source=gen,target=n,weight='length')
		nodevDrop[n] = nx.shortest_path_length(SG[gen],source=gen,target=n,weight='vDrop')
		nodeGrid[n] = gen

sorted_dist = sorted (nodedist.iteritems(), key=operator.itemgetter(1), reverse=True)
print "10 distros furthest from generator"
print "node\tgrid\tdistance(m)"
for x in range(10):
	print sorted_dist[x][0], '\t', nodeGrid[sorted_dist[x][0]], '\t', sorted_dist[x][1]

sorted_vDrop = sorted (nodevDrop.iteritems(), key=operator.itemgetter(1), reverse=True)
print "\n10 distros with worst voltage drop (50% of max current on all links)"
print "node\tgrid\tvDrop(Volt)"
for x in range(10):
	print sorted_vDrop[x][0], '\t', nodeGrid[sorted_vDrop[x][0]], '\t', sorted_vDrop[x][1]/1000

print
print "Count of distros by type"
print "Qty\tType"
for (a,b) in Counter(nodes.values()).items() :
	print b,'\t',a

print
print "Count of cable lengths by grid"
print "Grid\tType\tLength\tCount"

LL={}
for gen in gens:
	lt = nx.get_edge_attributes(SG[gen],'ltype')
	le = nx.get_edge_attributes(SG[gen],'length')
	for l in SG[gen].edges_iter():
		key = gen,lt[l],le[l]
		if key in LL:
			LL[key]+=1
		else:
			LL[key]=1

for a in LL.keys():
	# i am a knob
	print "%s\t%s\t%s\t%i"%(a[0],a[1],a[2],LL[a])

