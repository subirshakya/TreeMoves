
#!/usr/bin/env python

from __future__ import (division, print_function)
import random



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

	def node_dict(self,node,newdict={}):
		"""
		Returns dictionary with all nodes and branch lengths
		"""
		if node.children == []: #Terminal branch returns branch length
			newdict[node]=node.brl
			return newdict
		else:
			newdict[node]=node.brl #Add length of internal branch
			for child in node.children:
				self.node_dict(child) #Add length of terminal branch
			return newdict
			
data = "(A:3,((B:1,C:1):1,D:2):1)"
Sim = Tree(data)
dict = Sim.node_dict(Sim.root)
randomval = min(list(dict.values()))
print(randomval)
somevalue = []
for key, value in dict.items():
	if value == randomval:
		somevalue.append(key)
print(somevalue)
print(somevalue[0].children)