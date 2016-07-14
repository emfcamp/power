#!/usr/bin/env python
import json
import networkx as nx
import operator
from collections import Counter
import datetime

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

# if False, just link to any part of the nodes
linkspec=True

G = nx.DiGraph()
G.add_nodes_from(nodes)

for l in links:
        l_type = def_node[nodes[l['dst']]]['in']
        vDrop = def_link[l_type]['mvperM'] * l['length']
        mass = def_link[l_type]['density'] * l['length']
        G.add_edge(l['src'],l['dst'], length=l['length'], vDrop=vDrop, mass=mass, ltype=l_type)



def printdotfile(grid):
	GG = SG[grid]

	print """
digraph emfcamp_power_%s {
	node [shape=record]
	rankdir=LR
	nodesep=0.1
	fontname="ArialNarrow"
	graph [ resolution=300, fontname=ArialNarrow, fontcolor=blue, fontsize=8 ];
	node [ fontname=ArialNarrow, fontcolor=black, fontsize=10,margin=0];
	edge [ fontname=ArialNarrow, fontcolor=red, fontsize=10 ];
	"""%(grid)
	print """	#display title block
	title [shape=record, style="rounded,filled" margin=0.5 fillcolor="lightgray" label="EMF2016 Power|Grid: %s|%s"];
	"""%(grid, datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

	for curn in nx.nodes(GG):
		print """       # node %s type %s """ % (curn, nodes[curn])
		print """	%s [shape=none,label=<<table border="0" cellborder="1" cellspacing="0" cellpadding="0.5"><tr>""" % curn
		try: 
			opts = def_node[nodes[curn]]['out']
			rowspan = """ rowspan="%i" """% len(opts)
		except KeyError:
			rowspan = ''
			opts = []
		try: 
			inp = def_node[nodes[curn]]['in']
			print """		<td%s PORT="in"><font color="%s">%s</font></td>"""%(rowspan, def_link[inp]['color'], def_link[inp]['name'])
		except KeyError:
			pass
		print """		<td%s><font color="orange">%s</font><br/>%s</td>"""%(rowspan, curn, nodes[curn])
		for i, opt in enumerate(opts):
			if i>0 : print "		</tr><tr>" 
			if opt['count'] > 1: 
				label = "%ix%s"%(opt['count'],def_link[opt['port']]['name'])
			else:
				label = def_link[opt['port']]['name']
			if 'breaker' in opt:
				label += "<br/>%s"%(opt['breaker'])

			print """		<td port="%s"><font color="%s">%s</font></td>"""%(opt['port'],def_link[opt['port']]['color'],label)
		print "			</tr></table>> ]"
	ll_length = nx.get_edge_attributes(GG,'length')
	ll_type = nx.get_edge_attributes(GG,'ltype')
	
	for l in nx.edges(GG):

		print "#node ",l
		dst = l[1]
		src = l[0]
		## {u'src': u'A1', u'dst': u'A1_DK', u'length': 5}
		##         Kgen:"powerlock" -> Kdis:in [color="black" fontcolor="black" label="PL 5m" weight=20 penwidth=4]
		# get type of this link
		#l_type = def_node[nodes[l['dst']]]['in']
		l_type = ll_type[l]
		color = def_link[l_type]['color']
		name = def_link[l_type]['name']
		penwidth = def_link[l_type]['penwidth']
		weight = int(100 / ll_length[l]);
		leng = ll_length[l]/5
		# don't bother constraining input lines if its a tiny node
		if l_type=='32A' or l_type=='16A':
			c_in = ''
		else:
			c_in = ':in'
		if linkspec: 
			print """	%s:"%s" -> %s%s"""%(src,l_type,dst,c_in),
		else:
			print """	%s -> %s"""%(src,dst),
		print """[color="%s" fontcolor="%s" label="%s %im" weight=%i penwidth=%i len=%f]"""%(color,color,name,ll_length[l],weight,penwidth,leng)
		
		
	print "}"

SG={}
gens = {k for (k,v) in nodes.items() if v =='gen'}
for gen in gens:
        SG[gen] = G.subgraph( nx.node_connected_component(G.to_undirected(),gen) )
        printdotfile (gen)
