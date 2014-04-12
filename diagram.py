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

# if False, just link to any part of the nodes
linkspec=True

print """
digraph emfcamp_power {
        node [shape=record]
        rankdir=LR
	nodesep=0.02
	fontname="ArialNarrow"
        graph [ resolution=300, fontname=ArialNarrow, fontcolor=blue, fontsize=8 ];
        node [ fontname=ArialNarrow, fontcolor=black, fontsize=8,margin=0];
        edge [ fontname=ArialNarrow, fontcolor=red, fontsize=7 ];
"""

for curn in nodes:
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
		print """		<td port="%s"><font color="%s">%s</font></td>"""%(opt['port'],def_link[opt['port']]['color'],label)
	print "			</tr></table>> ]"

for l in links:
	## {u'src': u'A1', u'dst': u'A1_DK', u'length': 5}
	##         Kgen:"powerlock" -> Kdis:in [color="black" fontcolor="black" label="PL 5m" weight=20 penwidth=4]
	# get type of this link
	l_type = def_node[nodes[l['dst']]]['in']
	color = def_link[l_type]['color']
	name = def_link[l_type]['name']
	penwidth = def_link[l_type]['penwidth']
	weight = int(100 / l['length']);
	leng = l['length']/5
	# don't bother constraining input lines if its a tiny node
	if l_type=='32A' or l_type=='16A':
		c_in = ''
	else:
		c_in = ':in'
	if linkspec: 
		print """	%s:"%s" -> %s%s"""%(l['src'],l_type,l['dst'],c_in),
	else:
		print """	%s -> %s"""%(l['src'],l['dst']),
	print """[color="%s" fontcolor="%s" label="%s %im" weight=%i penwidth=%i len=%f]"""%(color,color,name,l['length'],weight,penwidth,leng)
	
print "}"

