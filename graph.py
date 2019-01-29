"""The <graph> module creates the main graph containting
   the transmitters and the transmission paths
   together with its subgraph (timeline)."""

from collections import defaultdict
import itertools
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from graphviz import Digraph

from ranking import rank_list, same_rank_subgraph, a_timeline


def draw_graph(path_to_transmitters_file,
               path_to_transmissions_file,
               timeline_step, color_origin=dict()):
    """Creates a graph with transmitters as nodes and transmission paths as edges.
       The following parameters must be provided:
       - a path to the csv file containing the transmitters
       - a path to the csv file containing the transmission
       - the time lapses in years that represent the timeline nodes (timeline_step)
       - (optional) a dictionary specifying colors for some or all of
         the origins, or 'auto' for automatic color assignment
    """
    
    assert path_to_transmissions_file.endswith('.csv') and\
           path_to_transmitters_file.endswith('.csv'), "Please provide .csv input files." 

    df_nodes = pd.read_csv(path_to_transmitters_file)
    
    df_edges = pd.read_csv(path_to_transmissions_file)
    
    df_nodes['Ranking'] = df_nodes.dAH // timeline_step

    # Creating the main graph
    
    g = Digraph('graph', filename='graph.gv',
                graph_attr=dict(size='12,24', fontsize='16',
                ranksep='1.2', concentrate='false'),
                node_attr=dict(shape='none'))
    

    if color_origin=='auto':
        cmap = plt.cm.get_cmap('tab20')
        colors = (mpl.colors.to_hex(cmap(i)) for i in range(20))
        color_cycle = itertools.cycle(colors)
        # Matching colors to origins
        color_origin = dict()
        for i, origin in enumerate(df_nodes.Origin.unique()):
            color_origin[origin] = next(color_cycle)   
    else:
        # every origin black except those in the color_origin parameter
        color_origin = defaultdict(lambda: 'black', color_origin)

    df_nodes['Color'] = df_nodes.Origin.map(color_origin)
        
    # Creating the nodes
    for _, row in df_nodes.iterrows():
        g.node(name=row.Transmitters, fontcolor=row.Color)

    # Defining the timeline subgraph attributes
    minimum = df_nodes.Ranking.min()
    maximum = df_nodes.Ranking.max()

    #Dictionary of nodes' attributes
    n_attr = {'name':'j', 'shape':'none'}

    #Dictionary of edges' attributes
    e_attr = {'arrowhead':'none', 'color':'black', 'penwidth':'10', 'len':'1.0'}

    # Creating the timeline as a subgraph
    a_timeline(g, minimum*timeline_step, maximum*timeline_step, timeline_step, n_attr, e_attr)

    #  Linking the nodes of the subgraph and the main graph together
    for rank in df_nodes.Ranking.unique():
        nodes_ranks = rank_list(str(rank*timeline_step), rank, df_nodes)
        same_rank_subgraph(g, nodes_ranks)

    # Creating the edges (transmission paths)
    for _, row in df_edges.iterrows():
        g.edge(row.From, row.To, arrowhead='vee')

    return g

def view_graph(path_to_transmitters_file,
               path_to_transmissions_file,
               timeline_step, color_origin=dict(),  graph_format='pdf'):
    """Displays the final graph (isnad tree) in the given format;
       The following parameters must be provided:
       - a path to the csv file containing the transmitters
       - a path to the csv file containing the transmission
       - the time lapses in years that represent the timeline nodes (timeline_step)
       - the export format: default 'pdf'; others: 'svg', 'png'
       - (optional) a dictionary specifying colors for some or all of
         the origins, or 'auto' for automatic color assignment
    """
    g = draw_graph(path_to_transmitters_file, path_to_transmissions_file, timeline_step, color_origin=color_origin)
    g.format=graph_format

    g.view()

