import networkx as nx
import community
import csv
from igraph import *

def g_newman_improved(G, important_edge=None):
    if G.number_of_edges() == 0:
            yield tuple(nx.connected_components(G))
            return
    if important_edge is None:
        def important_edge(G):
            betweenness = nx.edge_betweenness_centrality(G)
            return max(betweenness, key=betweenness.get)
    g = G.copy().to_undirected()
    g.remove_edges_from(g.selfloop_edges())
    _edge_removal_rep(g, important_edge)



def _edge_removal_rep(G, important_edge):
    G = G.copy().to_undirected()
    G.remove_edges_from(G.selfloop_edges())
    part = community.best_partition(G)
    mod = community.modularity(part, G)
    prev_mod = mod
    file_to_save = 'poblogs_cleaned'#raw_input('Filename to save in as... ')
    writer = csv.writer(open(file_to_save + '_Modularity_CDAs_Local_Maxima.csv', 'wb'))
    writer.writerow(['Edge Removed', 'EB', 'Next Edge To Be Removed',
                     'EB', 'Modularity', 'Community Size','Louvian',
                     'Label Propagation', 'Infomap', 'Walktrap',
                     'FastGreedy', 'Girvan-Newman'
                     ])
    count = 1
    #while G.number_of_edges() > 1:
    while prev_mod <= mod:
        prev_mod = mod
        eb_before_edge_removal = nx.edge_betweenness_centrality(G)
        edge = important_edge(G)
        edge_eb = eb_before_edge_removal[edge]
        G.remove_edge(*edge)
        eb_after_edge_removal = nx.edge_betweenness_centrality(G)
        edge1 = max(eb_after_edge_removal, key=eb_after_edge_removal.get)
        edge1_eb = eb_after_edge_removal[edge1]
        part = community.best_partition(G)
        mod = community.modularity(part, G)
        community_size, connected_components = nx.number_connected_components(G), nx.connected_components(G)
        communities = list()
        for i in connected_components:
            b = list(i)
            communities.append(b)
        filename = 'poblogs_cleaned'
        filename_len = len(file)
        if filename[:]
        #g = Graph().Read_Edgelist(filename+'.txt', directed=False)
        #g.simplify()
        g = Graph().Read_GML(filename+'.gml')
        g = g.to_undirected()
        g.remove_edges_from(g.selfloop_edges())

        if count:
            cda  = [

                str(g.community_multilevel()),
                str(g.community_label_propagation()),
                str(g.community_infomap()),
                str(g.community_walktrap().as_clustering()),
                str(g.community_fastgreedy().as_clustering()),
                str(g.community_edge_betweenness().as_clustering())
                ]

            writer.writerow([str(edge), edge_eb, str(edge1), edge1_eb,
                            mod, community_size, communities,
                            #0, cda[0], cda[1], cda[2], cda[3], cda[4]
                            cda[0], cda[1], cda[2], cda[3], cda[4],cda[5]
                            ])
            for i in cda:
                print i
            count = 0
        else:
            writer.writerow([str(edge), edge_eb, str(edge1), edge1_eb,
                            mod, community_size, communities])
    return mod

filename = 'poblogs_cleaned'#raw_input('Input edgelist file...    ')
#gx = nx.read_edgelist(filename+'.txt', nodetype=int)
gx = nx.read_gml(filename+'.gml')
res = tuple(g_newman_improved(gx))
print res