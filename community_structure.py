import sys
from collections import Counter


if (sys.argv[1] =="-n"):
	groups = int(sys.argv[2])
	filepath = sys.argv[3]
else:
	groups = 2
	filepath = sys.argv[1]

graph={}
global totaledges
#Read file data and store to dictionary
with open(filepath, "r") as file:
	for line in file:
		splittline = line.strip("\n").split(" ")
		try:
			graph[int(splittline[0])].append(int(splittline[1]))
		except KeyError:
			graph[int(splittline[0])]=[int(splittline[1])]

#complete undirected graph repesentation as dictionary	
graph_copy = graph.copy()		
for node,adj_nodes in graph_copy.items():
	for ad_node in adj_nodes:
		if (ad_node not in graph):
			graph[ad_node]=[node]
		elif (node not in graph[ad_node]):
			graph[ad_node].append(node)

totaledges = 0
for k,v in graph.items():
	totaledges+= len(v)

#dictionary with a values for each node
alpha={}
for k,v in graph.items():
	alpha[k] = len(v)/totaledges

'''Compute initial modularity(each node is a team itself) and there are not self links
all eii are 0. Thus modularity is the sum of -(ai^2)
'''
modularity = 0
for k,v in alpha.items():
	modularity-= pow(v,2)

def compute_alpha(group):
	# Helper function for group alpha values computation
	if (type(group) == int):
		return alpha[group]
	else:
		sumalpha=0
		for node in group:
			sumalpha+=alpha[node]
		return sumalpha


def find_best_pair(graph):
	#Returns the group pair which have the maximum dQ, plus the dQ value
	DQpairs ={}
	global totaledges
	for node,edges in graph.items():
		cnt = Counter()
		for edge in edges:
			cnt[edge]+=1
		for k,v in cnt.items():
			if (k,node) not in DQpairs.keys():
				alpha_node = compute_alpha(node)
				alpha_adj_node = compute_alpha(k)
				deltaQ =2*((v/totaledges)-(alpha_node*alpha_adj_node))
				DQpairs[(node),(k)] = deltaQ
	best_pair = max(DQpairs, key=DQpairs.get)
	return best_pair,DQpairs[best_pair]

def merge_groups(pair,graph_dict):
	#Returns the updated dictionary that derives after merging the two given groups
	if ((type(pair[0]) == tuple) and (type(pair[1]) == tuple)):
		new_group = pair[0] + pair[1]
	elif ((type(pair[0]) == tuple) and (type(pair[1]) == int)):
		new_group = pair[0] + (pair[1],)
	elif ((type(pair[0]) == int) and (type(pair[1]) == tuple)):
		new_group = (pair[0],) + pair[1]
	else:
		new_group = (pair[0],) + (pair[1],)
	graph_dict[new_group] = graph_dict.pop(pair[0])
	pair2_edges = graph_dict[pair[1]]
	graph_dict[new_group].extend(pair2_edges)
	del graph_dict[pair[1]]

	graph_dict[new_group] =list(filter(lambda x: x not in[pair[0],pair[1]],graph_dict[new_group]))
	
	graph_dict_copy = graph_dict.copy()		

	for k,v in graph_dict_copy.items():
		values = v
		for idx in range(len(values)):
			if ((values[idx] == pair[0]) or values[idx] == pair[1]):
				values[idx] = new_group
		graph_dict[k] = values
	return graph_dict



while(len(graph)!=groups):
	best_pair = find_best_pair(graph)
	graph = merge_groups(best_pair[0],graph)
	modularity += best_pair[1]


teams = []
for k,v in graph.items():
	if (type(k) ==tuple):
		team = list(k)
		team.sort()

	else:
		team = k
	teams.append(team)


for team in teams:
	print(team)

print("Q =",modularity)