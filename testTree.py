
#!/usr/bin/env python
'''
To Do:
comment everything before merging with master
make NNI script that calls tree and node classes
fix the weird additive issue with term node list method
change edge length to inverse edge lenght,a nd ammend tree traverse code
test if two windows wiht python still ahve tip list error. 
'''

#start with newick string
#turn into tree object
#get list of tips, stored as nodes
#get longest edge length
#get random number between 0 and edge length
#traverse tree starting at random tip, using random goal. 
#use this node as starting node for NNI
#this node will never be the root
#need to insure it is never a node between two tips.
#do NNI move


'''
## WHY IS THIS STORING THE PREVIOUS LISSSTTTT WHHHYYYYY
goo="(X:2,((Y:3,Z:1):2,W:8):6)"
Tim = Tree(goo)
Tim.printTermNodes(Tim.root)


bigD="(A:3,((B:1,C:1):1,D:2):1)"
Sim = Tree(bigD)
sim_tips = Sim.printTermNodes(Sim.root)
'''

-------------------------------------------------------
exit()

python

from __future__ import (division, print_function)
from readTree import Node
from readTree import Tree
import random
#makes a list of all children of a given node. 
def where_my_child(parent):
	children = []
	for child in parent.children:
		children.append(child)
	return children

def pick_tip(tree):
	#start with root unless you are starting at a specified internal node
	if n == 0:
		n=tree.root
	#if you arent at a tip. pick a child 
	while n.children !=[]:
		n = where_my_child(n)[random.choice([0,1])]
	return n


#pick a random goal to start NNI from.	
def pick_goal(tree, tip_list):
	# get list of tips as node objects. will put this back in when i fix bug.
	#tip_list = tree.printTermNodes(tree.root)
	edge_list = []
	# get list of all tip to root edges
	for node in tip_list:
		edge_list.append(tree.edge_length(node))
	long_edge = max(edge_list)
	#calculate goal, random number between 0 and longest edge.
	g = random.uniform(0,long_edge)
	print("goal: "+str(g))
	return g


#traverse nodes until you reach goal. If root is reached before goal. Return 0.
def traverse_nodes(node,goal):
	print("traverse node 1: "+str(node.name))
	if node.brl == 0:
		return node.brl
	else:
		#get inverse of branch length add back in after rewriting br macx function to be inverse
		#inv_br=1/float(node.brl)
		#subtract from goal
		goal -= node.brl
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


# pick random tip in tree. traverse backwards to goal. or start function over
def pick_start(tree, goal):
	#set root as start node
	n = tree.root
	#if not at tip, traverse until you hit a tip
	while n.children !=[]:
		n = where_my_child(n)[random.choice([0,1])]
		print("where kids: "+str(n.name))
	print("n: "+str(n.name))
	#begin at tip and stop at goal or root
	start = traverse_nodes(n,goal)
	#if you get to the root, recursion
	while start == 0:
		#recursive
		print("hit root -> recursion")
		return pick_start(tree,goal)
	print("start: "+str(start.name))
	return start

#import data and instantiate tree

doo="(P:9,(Q:7,(X:2,((Y:3,Z:1):2,W:8):6):3):4)"
Jim = Tree(doo)
#Tim_tips = Tim.printTermNodes(Tim.root)
g = pick_goal(Jim,Jim_tips)
x = pick_start(Jim,g)
#tests
x=Jim_tips[0]
x.name
y=Jim_tips[1]
y.name
Tim.edge_length(x)

### make into choose random tip funciton
tip_list = Jim.list_term_nodes(Jim.root)
random_tip = random.choice(tip_list)



#import data and instantiate tree

goo="(X:2,((Y:3,Z:1):2,W:8):6)"
Tim = Tree(goo)
#Tim_tips = Tim.printTermNodes(Tim.root)
g = pick_goal(Tim,Tim_tips)
x = pick_start(Tim,g)
#tests
x=Tim_tips[0]
x.name
y=Tim_tips[1].
y.name
Tim.edge_length(x)




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