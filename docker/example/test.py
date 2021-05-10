from graphspace_python.api.client import GraphSpace
from graphspace_python.graphs.classes.gsgraph import GSGraph
import networkx as nx
import time
import sys

def main(graph_file,username,password):

	# read file as networkx graph
	nxG = nx.read_edgelist(graph_file)

	# convert networkx graph to GraphSpace object
	G = GSGraph()
	G.set_name('Docker Example %.4f' % (time.time()))
	for n in nxG.nodes():
		G.add_node(n,label=n,popup='Node %s' % (n))
		G.add_node_style(n,color='#ACCE9A',shape='rectangle',width=30,height=30)
	for u,v in nxG.edges():
		G.add_edge(u,v,popup='Edge %s-%s' % (u,v))
		G.add_edge_style(u,v,width=2,color='#281D6A')

	# post with unique timestamp
	gs = GraphSpace(username,password)
	try:
		graph = gs.update_graph(G)
	except:
		graph = gs.post_graph(G)
	print('posted graph')
	return

if __name__ == '__main__':
	if len(sys.argv) != 4:
		print('USAGE: python test.py <GRAPH_FILE> <USERNAME> <PASSWORD>\n\n\twhere <USERNAME> and <PASSWORD> are GraphSpace username and password.')
		print('CURRENT ARGS:',sys.argv)
		sys.exit()

	main(sys.argv[1],sys.argv[2],sys.argv[3])
