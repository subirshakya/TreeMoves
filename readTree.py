
#!/usr/bin/env python

from __future__ import (division, print_function)
import random
import numpy


"""pass a node to node. Node("root")"""
"""root.children will give children of node"""
class Node:
	"""pass a node to node. Node("root")"""
	"""root.children will give children of node"""
	def __init__(self,name="",parent=None,children=None, branchlength = 0):
		"""name of node"""
		self.name = name
		self.brl = branchlength
		if parent is None:
			self.parent = []
		else:
			self.parent = parent
		if children is None:
			self.children = []
		else:
			self.children = children
		
class Tree:
	"""
	Defines a class of phylogenetic tree, consisting of linked Node objects.
	"""

	def __init__(self, data, ndict=None, terminal_nodes=None):
		"""variable stores object called root that is classified as a node"""
		self.root = Node("root") #Define root
		"""Initiate with self.root as base. First step is initiating data with root as parent of ALL"""
		self.newick_splicer(data.strip(";"), self.root)

	def newick_splicer(self, data, parent):
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
							if unit.find(":") != -1: #For cases with branch lengths
								d = unit[0:unit.rfind(":")] #get rid of trailing branchlength if provided. rfind from the right side
								node_creater = Node(d, parent = parent) #Create node entry
								node_creater.brl = float(unit[unit.rfind(":")+1:]) #Append branch length of that branch
								parent.children.append(node_creater) #Create children. Hello parent, your children are ...
								self.newick_splicer(d, node_creater) #Recursive function
							else: #For case with no branch lengths
								d=unit
								node_creater = Node(d, parent = parent)
								parent.children.append(node_creater)
								self.newick_splicer(d, node_creater)
						break #Terminate loop, we don't need to look any further

	def print_names(self,node):
		"""
		A method of a Tree object that will print out the names of its
		terminal nodes.
		"""

		if node.children == []: #Identifies terminal node
			print (node.name)
		else:
			for child in node.children:
				self.print_names(child)
	
	def list_term_nodes(self,node,terminal_nodes=None):
		"""
		A method of a Tree object that will print out the node instances for all tips in a list. 
		"""
		if terminal_nodes is None:
			terminal_nodes=[]
		if node.children == []: #Identifies terminal node
			print(node.name)
			terminal_nodes.append(node)
		else:
			for child in node.children:
				print(terminal_nodes)
				self.list_term_nodes(child,terminal_nodes)
		return terminal_nodes
	
	def inv_edge_len(self,node,edge=0):
		"""
		A method of a Tree object that will return the total length from given node to root. 
		"""
		#at root return total
		if node.brl == 0:
			return edge 
		else:
			#add branch length
			edge += 1/float(node.brl)
			new_node = node.parent
			return self.inv_edge_len(new_node,edge)

	def tree_len(self,node):
		"""
		A method to calculate and return total tree length.
		"""

		tot_len = 0
		if node.children == []: #Terminal branch returns branch length
			return node.brl
		else:
			tot_len += node.brl #Add length of internal branch
			for child in node.children:
				tot_len += self.tree_len(child) #Add length of terminal branch
			return tot_len

	def inv_tree_len(self,node):
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
					inv_tot_len += self.inv_tree_len(child)
				return inv_tot_len
			else:
				inv_tot_len += 1/float(node.brl) #Add length of internal branch
				for child in node.children:
					inv_tot_len += self.inv_tree_len(child) #Add length of terminal branch
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

	def has_grandkids(self,node):
		"""
		Takes a node and will randomy choose a child and return the child node if it has grandchildren
		could add an argument to determine if the child is chosen randomly or based on branch length of children. (for passing shorter branches to NNI moves more often).
		"""
		#if node has children
		if node.children != []:
			#pick random child
			kid = node.children[random.choice([0,1])]
			#if child has children, return grandchildren of node
			if kid.children != []:
				return kid
			else:
				return self.has_grandkids(node)
		#if node doesnt have children, you are at a tip
		else:
			return 0

	def node_dict(self,node,ndict=None):
 		"""
 		Returns dictionary with all nodes and branch lengths
 		"""
 		if ndict is None:
			ndict={}
 		if node.children == []: #Terminal branch returns branch length
 			ndict[node]=node.brl
 			return ndict
 		else:
 			ndict[node]=node.brl #Add length of internal branch
 			for child in node.children:
 				self.node_dict(child,ndict) #Add length of terminal branch
 			return ndict
 			
def pick_start_node(tree):
	n_dict = tree.node_dict(tree.root)
	#get goal chosen from exp distribution
	goal = numpy.random.exponential(0.1)
	#get node closest to goal, coming from zero towards goal
	start_brl = max(brl for brl in list(n_dict.values()) if brl < goal)#could also come from above, or choose randomly to come from above or below. 
	for key, value in n_dict.items():
		if value == start_brl:
				start_node = key
	return start_node

def pickier_start_node(tree):
	#get dictionary of nodes,branchlen as key,value
	start_node = tree.root
	#if goal is between 0 and shortest branch, or returns a tip node
	while start_node.brl == 0 or start_node.children == []:
		start_node = pick_start_node(tree)
	#if returns a node to sister tips, redo
	if start_node.parent.brl == 0:
		start_node = pickier_start_node(tree)
	return start_node  

def NNI(tree):
	'''
	Does NNI move on random branch, preferentially choosing smaller branches. Returns altered tree. 
	'''
	#reassign start node to c2. assign as c2
	c2 = pickier_start_node(tree)
	p = c2.parent
	#print("c2 = "+str(c2.name))
	#print("p = "+str(p.name))
	#assign other child to c1
	for c in p.children:
			if c != c2:
				c1 = c
	#c2 will be the node for the brl we choose, so it will always have children. c1 is the other child for the parent/start node
	#store branchlengths 
	br1 = c1.brl
	br2 = c2.brl
	#we don't technically need to store these because they are all still attached to c2, but doing it for clarity for now.
	gc1 = c2.children[0]
	gc2 = c2.children[1]
	br3 = gc1.brl
	br4 = gc2.brl
	#remove all children
	p.children = []
	name = "new_"+str(c2.name)
	#this is the node to attach things to
	new_node = Node(name,parent=p)
	#give it branchlength of c2, then start adding branches
	new_node.brl = br2
	#add new node to parent
	p.children.append(new_node)
	#add c1 to new node
	new_node.children.append(c1)
	#add grandkids, one to parent, one to new node. randomly. 
	adopt=random.choice([1,2])
	if adopt == 1:
		p.children.append(gc1)
		new_node.children.append(gc2)
	elif adopt ==2:
		p.children.append(gc2)
		new_node.children.append(gc1)
	#name=tree.newick(new_node)
	#new_node = can I rename node? this would keep with node naming scheme
	return tree