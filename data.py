
import sys
import os
import re

log = os.popen('git log').read().split('\n')
log = list(filter(lambda x: re.match('commit [0-9a-f]{5,40}',x) != None or x[:6] == 'Author', log))
log = list(map(lambda x: x.split(' ')[1].lower() if x[:6] == 'Author' else x.split(' ')[1], log))
log = list(zip(log[1:len(log):2], log[0:len(log):2]))
activity = {}
for l in log:
	out = os.popen('git diff '+l[1]+' --numstat').read().split('\n')
	for o in out:
		print(l)
		print(o)



# [print(l) for l in log]

rootDir = '.'
fileList = []

for dir_, _, files in os.walk(rootDir):
    for fileName in files:
        relDir = os.path.relpath(dir_, rootDir)
        relFile = os.path.join(relDir, fileName)
        fileList.append(relFile)

fileList = list(filter (lambda x: x.split('/')[0] != '.git', fileList))
fileList = map(lambda x: x[1:] if x[0] == '.' else '/'+x, fileList)
[print(f) for f in fileList]

class Node:

	def __init__(self, path):
		self.path = path
		self.contributions = {}
		self.files = []

def getNode(node, path):
	if node.path == path: return node
	parent = None
	for c in node.files:
		parent = get_node(c, path)
	return parent

def addNode(node, childPath, parentPath):
	child = Node(childPath)
	parent = getNode(node, parentPath)
	parent.files.append(child)

def populateTree(root, data):
	for d in data:
		idx = d.path.rfind('/')
		parent = '/'
		if (idx > 0) parent = data.path[:idx]
		addNode(root, d.path, parent)