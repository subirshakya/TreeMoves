
#!/usr/bin/env python

#start with newick string
#turn into tree object
#get list of tips, stored as nodes
#get longest edge length
#get random number between 0 and edge length
#traverse tree starting at random tip, using random goal. 
#use end point as starting node for NNI
#do NNI move



-------------------------------------------------------
exit()

python

from __future__ import (division, print_function)
from readTree import Node
from readTree import Tree
import random
#where my children
def where_my_child(parent):
	children = []
	for child in parent.children:
		children.append(child)
	return children

#import data and instantiate tree
bigD="(A:3,((B:1,C:1):1,D:2):1)"
Sim = Tree(bigD)
sim_tips = Sim.printTermNodes(Sim.root)

## WHY IS THIS STORING THE PREVIOUS LISSSTTTT WHHHYYYYY
goo="(X:2,((Y:3,Z:1):2,W:8):6)"
Tim = Tree(goo)
Tim.printTermNodes(Tim.root)






-----pick node to start------


edge_list = []
for node in tip_list:
	edge_list.extend([node,edge_length(node)])

def edge_length(node,edge=0):
	if node.brl == 0:
		return edge 
	else:
		#add branch length
		edge += node.brl
		new_node = node.parent
		return edge_length(new_node,edge)

def traverse_nodes(node,goal):
	if node.brl == 0:
		return node.brl
	else:
		#get inverse of branch length
		inv_br=1/float(node.brl)
		#subtract from goal
		goal -= inv_br
		#print("new goal:"+str(goal))
		#if goal is less than zero, return p as node you will start NNI with. 
		if goal <= 0:
			start = node
			#print("start: "+str(start.name))
			return start
		#if goal is still above 0, go to parent node and run program again
		elif goal > 0:
			p = node.parent
			#print("new parent: "+str(p.name))
			return traverse_nodes(p,goal)


def pick_start(tree):
	#set root as start node for picking terminal node to start with
	n=Sim.root
	#calculate total inverse tree length
	invTL = Sim.inverseTreeLength(n)
	#print("inv_TL = "+str(invTL))
	#calculate goal, random number between 0 and invTL to use for picking a random node to do NNI move on. 
	g = random.uniform(0,invTL)
	#print("OG goal = "+str(g))
	#find a terminal node (randomly) and assign to n
	while n.children !=[]:
		n = where_my_child(n)[random.choice([0,1])]
	#print("first node: "+str(n.name))
	#find a node based on the goal
	c1 = traverse_nodes(n,g)
	#print("first c1: "+str(c1))
	#print(type(c1))
	#if you get to the root and return false
	while c1 == 0:
		#rerun terminal node choice and traversing tree
		n=Sim.root
		while n.children !=[]:
			n = where_my_child(n)[random.choice([0,1])]
		print("false loop node: "+str(n.name))
		c1=traverse_nodes(n,g)
	p = c1
	#print("p: "+str(p.name))
	return p

x = pick_start(Sim)

-----older_tests-------------------------------------------------
n=Sim.root
#calculate total inverse tree length
invTL = Sim.inverseTreeLength(n)
print("inv_TL = "+str(invTL))
#calculate goal, random number between 0 and invTL to use for picking a random node to do NNI move on. 
g = random.uniform(0,invTL)
print("OG goal = "+str(g))
#find a terminal node (randomly) and assign to n
while n.children !=[]:
	n = where_my_child(n)[random.choice([0,1])]

x = traverse_nodes(n,g)


#pick a terminal node
#traverse nodes, updating goal, until goal < 0
#if we reach the root before hitting our goal, 
#pick a new terminal node





----NNI moves-------------------------------------------------------------
loop = "true"
while loop == "true":
	#start with root
	c1=Sim.root
	#find a terminal node (randomly) and assign to c1
	while c1.children !=[]:
		c1 = where_my_child(c1)[random.choice([0,1])]
	#print c1.name
	#for both childrens of the parent of c1, assign name to c2
	for c in c1.parent.children:
		if c != c1:
			c2 =c
	br1, br2 = c1.brl, c2.brl
	#only works if c2 has grand children. Can't NNI on sister taxa only.
	if c2.children != []:
		gc1, gc2 = where_my_child(c2)	
		br3, br4 = gc1.brl, gc2.brl
		loop = "false"
		
p = c1.parent
#remove all children
p.children = []
#this is the node to attach grandchildren to
new_node = Node("new",parent=p)
#give it same br as before
new_node.brl = br2
#append one of the two grandchildren to p. append other one to new node
adopt=random.choice([1,2])
if adopt == 1:
	p.children.append(gc1)
	new_node.children.append(gc2)
elif adopt ==2:
	p.children.append(gc2)
	new_node.children.append(gc1)
p.children.append(new_node)
#add c1 to new node
new_node.children.append(c1)