"""The <graph> module draws the final graph creating 
and connecting all the nodes together with edges 
and aligning them to the timeline subgraph."""

#Import modules
from graphviz import Digraph
import pandas as pd
##from paths import path_all, creates_edges
from ranking import rank_list, same_rank_subgraph, a_timeline

def draw_graph(timeline_step, path_to_transmitters_file, path_to_transmissions_file, pdf=True):
    """draws the final graph by
        (1) creating a dataframe with nodes (transmitters) using the
        database_to_dataframe function;
        (2) creating the edges (transmission path) using the
        database_to_dataframe function;
        (3) ranking the nodes to match them with the timeline subgraph;
        (4) creating the graph as <g>;
        (5) creating the nodes within <g>;
        (6) defining the timeline subgraph attributes;
        (7) creating the timeline subgraph with a_timeline function;
        (8) linking the nodes of the subgraph and the main graph together
            with the functions rank_list and same_rank_subgraph;
        (9) drawing the edges.
        The output is a graph in pdf format.
        """
    #1#
    assert path_to_transmissions_file.endswith('.csv') and\
           path_to_transmitters_file.endswith('.csv'), "Please provide .csv input files." 
    df_nodes = pd.read_csv(path_to_transmitters_file)
    #2#
    df_edges = pd.read_csv(path_to_transmissions_file)
    #3#
    df_nodes['Ranking'] = df_nodes.dAH // timeline_step
    #4#
    g = Digraph('graph', filename='graph.gv',
                graph_attr=dict(size='12,24', fontsize='16',
                ranksep='1.2', concentrate='false'),
                node_attr=dict(shape='none'))
    
    #5# Creating the nodes
    for _, row in df_nodes.iterrows():
        g.node(name=row.Transmitters, fontcolor='   black')

    #6# Defining the timeline subgraph attributes
    minimum = df_nodes.Ranking.min()
    maximum = df_nodes.Ranking.max()

    #Dictionary of nodes' attributes
    n_attr = {'name':'j', 'shape':'none'}

    #Dictionary of edges' attributes
    e_attr = {'arrowhead':'none', 'color':'black', 'penwidth':'10', 'len':'1.0'}

    #7# Creating the timeline (subgraph)
    a_timeline(g, minimum*timeline_step, maximum*timeline_step, timeline_step, n_attr, e_attr)
    #8# Linking the nodes of the subgraph and the main graph together
    for rank in df_nodes.Ranking.unique():
        nodes_ranks = rank_list(str(rank*timeline_step), rank, df_nodes)
        same_rank_subgraph(g, nodes_ranks)

    #9# Drawing the edges (transmission paths)
    for _, row in df_edges.iterrows():
        g.edge(row.From, row.To, arrowhead='vee')

    if pdf:
        g.view()
    return g
    #return g.view() if pdf else g
