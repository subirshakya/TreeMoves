
#!/usr/bin/env python

from __future__ import (division, print_function)
from scipy.linalg import expm
import numpy


"""pass a node to node. Node("root")"""
"""root.children will give children of node"""
class Node:
	"""pass a node to node. Node("root")"""
	"""root.children will give children of node"""
	def __init__(self,name="",parent=None,children=None, branchlength = 0, sequence = None):
		"""name of node"""
		self.name = name
		if parent is None:
			self.parent = []
		else:
			self.parent = parent
		if children is None:
			self.children = []
		else:
			self.children = children
		self.brl = branchlength


class Tree:
	"""
	Defines a class of phylogenetic tree, consisting of linked Node objects.
	"""

	def __init__(self, data):
		"""variable stores object called root that is classified as a node"""
		self.root = Node("root") #Define root
		"""Initiate with self.root as base. First step is initiating data with root as parent of ALL"""
		self.newicksplicer(data, self.root)

	def newicksplicer(self, data, parent):
		"""
		Splices newick data to create a node based tree.
		"""
		data = data.replace(" ", "")[1: len(data)] 	 #Get rid of all spaces and removes first and last parenthesis
		n = 0
		if data.count(",") != 0: #While there are comma separated taxa
			for key in range(len(data)): #Find the corresponding comma for a given parenthesis (n will be 0 for the correct comma)
				if data[key] == "(":
					n += 1 #Increase index of n by 1 for 1 step into new node
				elif data[key] == ")":
					n -= 1 #Decrease index of n by 1 for 1 step outout node
				elif data[key] == ",":
					if n == 0: #To check for correct comma
						vals = (data[0:key], data[key+1:len(data)-1]) #Break newick into left and right datasets
						for unit in vals: #For each entry of dataset
							if unit[-1] != ")": #For cases with branch lengths
								d = unit[0:unit.rfind(":")] #get rid of trailing branchlength if provided. rfind from the right side
								node_creater = Node(d, parent = parent) #Create node entry
								node_creater.brl = float(unit[unit.rfind(":")+1:]) #Append branch length of that branch
								parent.children.append(node_creater) #Create children. Hello parent, your children are ...
								self.newicksplicer(d, node_creater) #Recursive function
							else: #For case with no branch lengths
								d=unit
								node_creater = Node(d, parent = parent)
								parent.children.append(node_creater)
								self.newicksplicer(d, node_creater)
						break #Terminate loop, we don't need to look any further

	def printNames(self,node):
		"""
		A method of a Tree object that will print out the names of its
		terminal nodes.
		"""

		if node.children == []: #Identifies terminal node
			print (node.name)
		else:
			for child in node.children:
				self.printNames(child)

	def treeLength(self,node):
		"""
		A method to calculate and return total tree length.
		"""

		tot_len = 0
		if node.children == []: #Terminal branch returns branch length
			return node.brl
		else:
			tot_len += node.brl #Add length of internal branch
			for child in node.children:
				tot_len += self.treeLength(child) #Add length of terminal branch
			return tot_len

	def inverseTreeLength(self,node):
		"""
		A method to calculate and return inverse of total tree length.
		"""

		inv_tot_len = 0
		if node.children == []: #Terminal branch returns branch length
			inv_tot_len = 1/float(node.brl)
			return inv_tot_len
		else:
			if node.brl == 0: #otherwise we get an error for root
				inv_tot_len += 0
				for child in node.children:
					inv_tot_len += self.inverseTreeLength(child)
				return inv_tot_len
			else:
				inv_tot_len += 1/float(node.brl) #Add length of internal branch
				for child in node.children:
					inv_tot_len += self.inverseTreeLength(child) #Add length of terminal branch
				return inv_tot_len

	def newick(self,node):
		"""
		A method of a Tree object that will print out the Tree as a
		parenthetical string (Newick format).
		"""

		newick = "(" #Opening bracket
		if node.children == []: #Terminal branch returns name
			return node.name + ":" + str(node.brl)
		else:
			for child in node.children:
				if node.children[-1] == child: #Don't add commas to last entry
					newick += self.newick(child)
				else:
					newick += self.newick(child) + "," #Adds commas to non-last entries
			if node.brl != 0:
				newick += "):" + str(node.brl) #Adds closing bracket
			else:
				newick += ")"
			return newick

-------------------------------------------------------
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

-----pick node to start------


def traverse_nodes(node,goal):
	if node.brl == 0:
		print("br len is zero")
		return 56
	else:
		#get inverse of branch length
		inv_br=1/float(node.brl)
		#subtract from goal
		goal -= inv_br
		print("new goal:"+str(goal))
		#if goal is less than zero, return p as node you will start NNI with. 
		if goal <= 0:
			start = node
			print("start: "+str(start.name))
			return start
		#if goal is still above 0, go to parent node and run program again
		elif goal > 0:
			p = node.parent
			print("new parent: "+str(p.name))
			traverse_nodes(p,goal)


def pick_start(tree):
	#set root as start node for picking terminal node to start with
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
	print("first node: "+str(n.name))
	#find a node based on the goal
	c1 = traverse_nodes(n,g)
	print("first c1: "+str(c1))
	#if you get to the root and return false
	while c1 == 0:
		#rerun terminal node choice and traversing tree
		n=Sim.root
		while n.children !=[]:
			n = where_my_child(n)[random.choice([0,1])]
		print("false loop node: "+str(n.name))
		c1=traverse_nodes(n,g)
	p = c1
	print("p: "+str(p.name))
	return p

pick_start(Sim)

-----test-------
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