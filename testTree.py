
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
#write in a way to make sure you dont make the same replicate trees with multiple moves? or not? 

#write method to choose start based on list of all branchlenghts0

#picking tip first and then traversing backwards. could bias towards specious clades. 


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
import numpy


 
def pick_start(tree, goal):
	#set root as start node
	n = random_tip(tree, tip_list)
	#begin at tip and stop at goal or root
	node1 = traverse_nodes(n,goal)
	start = node1.parent
	#if you get to the root, recursion
	if start == 0:
		print("hit root -> recursion")
		return pick_start(tree,goal,tip_list)
	#if start is a tip node, recursion
	elif start.children == [] :
		print("tip node -> recursion")
		return pick_start(tree,goal,tip_list)
	#if start is node to sister tips, recursion
	elif start.children[0].children == [] and start.children[1].children == []:
		print("node to sisters -> recursion")
		return pick_start(tree,goal,tip_list)
	else:
		print("start: "+str(start.name))
		return start

#import data and instantiate tree

doo="(P:9,(Q:7,(X:2,((Y:3,Z:1):2,W:8):6):3):4)"
Jim = Tree(doo)
#tip_list = Jim.list_term_nodes(Jim.root)
g = pick_goal(Jim,tip_list) #Z to root is longest
x = pick_start(Jim,g,tip_list)


data = "(A:3,((B:1,C:1):1,D:2):1)"
Sim = Tree(data)
#get dictionary of nodes,branchlen as key,value
nodedict = Sim.node_dict(Sim.root)
#
randomval = min(list(dict.values()))
#get minimum brl
minbrl = min(list(nodedict.values()))
maxbrl = max(list(nodedict.values()))
numpy.random.exponential
print(randomval)
somevalue = []
for key, value in nodedict.items():
	if value == randomval:
		somevalue.append(key)
print(somevalue)
print(somevalue[0].children) 

'''
node = get random node
goal = pick random number from exp dist wiht same rate as brl prior
min(x for x in my_list if x > goal)

'''

#store brl and children for all nodes involved before any moves are made. only need to store the node, it has all further info attached to it already. because of the nature of the tree class set up. 
#currently node names will still reflet the original children, not the new ones. this might actually be useful in racking what has happened. 

----NNI moves-------------------------------------------------------------
p = x
tree = Jim

def NNI(start,tree):
	#pick child node with children. 
	if start.children[0].brl < start.children[1].brl and start.children[0] 
	c2 = tree.has_grandkids(start)
	#assign other child to c1
	for c in start.children:
			if c != c2:
				c1 = c
	#c2 will always be the child that we are grabbing children with to do NNI with. c1 could also have children, but we are ignoring them. 
	#store branchlengths 
	br1 = c1.brl
	br2 = c2.brl
	#we don't technically need to store these because they are all still attached to c2, but doing it for clarity for now.
	gc1 = c2.children[0]
	gc2 = c2.children[1]
	br3 = gc1.brl
	br4 = gc2.brl
	#remove all children
	start.children = []
	#this is the node to attach things to
	new_node = Node("new",parent=start)
	#give it branchlength of c2, then start adding branches
	new_node.brl = br2
	#add new node to parent
	start.children.append(new_node)
	#add c1 to new node
	new_node.children.append(c1)
	#add grandkids, one to parent, one to new node. randomly. 
	adopt=random.choice([1,2])
	if adopt == 1:
		start.children.append(gc1)
		new_node.children.append(gc2)
	elif adopt ==2:
		start.children.append(gc2)
		new_node.children.append(gc1)
	return tree

