# pick random tip in tree. traverse backwards to goal. or start
def pick_start(tree, goal, n=tree.root):
	#set root as start node
	n=tree.root
	#start at root, find children until there are no more children.
	while n.children !=[]:
		n = where_my_child(n)[random.choice([0,1])]
		print("where kids: "+str(n.name))
	print("first n: "+str(n.name))
	#find a node based on the goal
	start = traverse_nodes(n,goal)
	print("first start: "+str(start))
	#if you get to the root
	while start == 0:
		#pick another tip, start at root
		while n.children !=[]:
			n = where_my_child(tree.root)[random.choice([0,1])]
		print("n : "+str(n.name))
		#pick another random node based on goal
		start=traverse_nodes(n,goal)
		#print("start: "+str(start))
	#print("p: "+str(p.name))
	return start


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
		
--------------------------------------------------------

		# pick random tip in tree. traverse backwards to goal. or start function over
def pick_start(tree, goal, n=0):
	#set root as start node
	if n == 0:
		n=tree.root
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
		return pick_start(tree,goal,tree.root)
	print("start: "+str(start.name))
	return start
