
import os
import re

EMPTY = '4b825dc642cb6eb9a060e54bf8d69288fbee4904'

log = os.popen('git log').read().split('\n')
log = list(filter(lambda x: re.match('commit [0-9a-f]{5,40}',x) != None or x[:6] == 'Author', log))
log = list(map(lambda x: x.split(' ')[1].lower() if x[:6] == 'Author' else x.split(' ')[1], log))
log = list(zip(log[1:len(log):2], log[0:len(log):2]))
activity = dict(map(lambda x: (x[0], {}), log))
for i in range(len(log)):
	if i < len(log)-1:
		out = os.popen('git diff '+log[i][1]+' '+log[i+1][1]+' --numstat').read().split('\n')
	else:
		out = os.popen('git diff '+log[i][1]+' '+EMPTY+' --numstat').read().split('\n')
	user = log[i][0]
	for o in out[:-1]:
		ol = o.split('\t')
		changes = int(ol[0])+int(ol[1])
		k = '/'+ol[2]
		if k in activity[user]:
			activity[user][k] += changes
		else:
			activity[user][k] = changes

# print(activity)

# for l in log: print(l)

rootDir = '.'
fileList = []

cmd = """ls -R """+rootDir+""" | awk '/:$/&&f{s=$0;f=0}/:$/&&!f{sub(/:$/,"");s=$0;f=1;next}NF&&f{ print s"/"$0 }'"""
fileList = os.popen(cmd).read().split('\n')
fileList = list(map(lambda x: x[1:], fileList))
fileList = sorted(fileList, key=lambda x: x.count('/'))[1:]

# for f in fileList: print(f)

class Node:

	def __init__(self, path):
		self.path = path
		self.contributions = {}
		self.files = []

def getNode(node, path):
	if node.path == path: return node
	parent = None
	for c in node.files:
		parent = getNode(c, path)
		if parent != None: break
	return parent

def addNode(node, childPath, parentPath):
	child = Node(childPath)
	parent = getNode(node, parentPath)
	parent.files.append(child)

def populateTree(root, data):
	for d in data:
		idx = d.rfind('/')
		parent = '/'
		if (idx > 0): parent = d[:idx]
		addNode(root, d, parent)

def combineDicts(d1, d2):
	result = {}
	for k in d1: result[k] = d1[k]
	for k in d2:
		if k in result:
			result[k] += d2[k]
		else:
			result[k] = d2[k]
	return result

def extractActivity(path):
	result = {}
	for user in activity:
		if path in activity[user]:
			result[user] = activity[user][path]
	return result

def getContributions(node):
	if len(node.files) == 0:
		node.contributions = extractActivity(node.path)
		return node.contributions
	for c in node.files:
		node.contributions = combineDicts(node.contributions, getContributions(c))
	return node.contributions

root = Node('/')
populateTree(root, fileList)
getContributions(root)

import json
import pprint

json = json.dumps(root, default=lambda o: o.__dict__, sort_keys=False, indent=4, separators=(',', ': '))

print(json)