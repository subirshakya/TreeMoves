
#!/usr/bin/env python
'''
To Do:
'''

#write in a way to make sure you dont make the same replicate trees with multiple moves? or not? 
#write a function to import from file and export as newick to file
#write wrapper to run x number of nni moves
#in that wrapper add option for no duplicates. use dendropy to compare newick topologies with RF dist or something. 

-------------------------------------------------------
exit()

python

from __future__ import (division, print_function)
from readTree import Node
from readTree import Tree
import random
import numpy
import readTree

doo="(P:0.09,(Q:0.07,(X:0.02,((Y:0.03,Z:0.01):0.02,W:0.08):0.06):0.03):0.04)"
Jim = Tree(doo)
Zim = Tree(doo)
Jim.newick(Jim.root)
Zim.newick(Zim.root)
readTree.NNI(Zim)
Jim.newick(Jim.root)
Zim.newick(Zim.root)

data = "(A:0.3,((B:0.05,C:0.1):0.15,D:0.2):0.5)"
Sim = Tree(data)


for key, value in Jim.node_dict(Jim.root).items():
	print(key.name)



