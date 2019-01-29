"""The <graph> module creates the main graph containting
   the transmitters and the transmission paths
   together with its subgraph (timeline)."""

from graphviz import Digraph
import pandas as pd
from ranking import rank_list, same_rank_subgraph, a_timeline


def draw_graph(path_to_transmitters_file, path_to_transmissions_file, timeline_step):
    """Creates a graph with transmitters as nodes and transmission paths as edges.
       The following parameters must be provided:
       - a path to the csv file containing the transmitters
       - a path to the csv file containing the transmission
       - the time lapses in years that represent the timeline nodes (timeline_step)
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
    
    
    for _, row in df_nodes.iterrows():
        g.node(name=row.Transmitters, fontcolor='black')

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

    # Drawing the edges (transmission paths)
    for _, row in df_edges.iterrows():
        g.edge(row.From, row.To, arrowhead='vee')

    return g

def view_graph(path_to_transmitters_file, path_to_transmissions_file, timeline_step, graph_format):
    """Displays the final graph (isnad tree) in the given format;
       The following parameters must be provided:
       - a path to the csv file containing the transmitters
       - a path to the csv file containing the transmission
       - the time lapses in years that represent the timeline nodes (timeline_step)
       - the export format: 'svg', 'pdf', 'png'
    """
    g = draw_graph(path_to_transmitters_file, path_to_transmissions_file, timeline_step)
    g.format=graph_format

    g.view()

