r"""The <graph> module draws the final graph creating 
and connecting all the nodes together with edges 
and aligning them to the timeline subgraph."""

import pandas as pd
from graphviz import Digraph
from ranking import rank_list, same_rank_subgraph, a_timeline


def draw_graph(path_to_transmitters_file:str,
               path_to_transmissions_file:str,
               timeline_step:int, color_origin=dict()) -> Digraph:
    """
    draws the final graph by
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
    assert path_to_transmissions_file.endswith('.csv') and\
           path_to_transmitters_file.endswith('.csv'), "Please provide .csv input files."

    # init dataframes from files
    df_nodes = pd.read_csv(path_to_transmitters_file)
    df_edges = pd.read_csv(path_to_transmissions_file)
    # create ranking ids
    df_nodes['Ranking'] = df_nodes.dAH // timeline_step



    # Creating the main graph    
    g = Digraph('graph', filename='graph.gv',
                graph_attr=dict(size='12,24', fontsize='16',
                ranksep='1.2', concentrate='false'),
                node_attr=dict(shape='none'))
    
    # TODO more colors
    color_origin = 'black'
    df_nodes['Color'] = color_origin
        
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
    for rank in range(df_nodes.Ranking.unique().max()+1):
        nodes_ranks = rank_list(str(rank*timeline_step), rank, df_nodes)
        same_rank_subgraph(g, nodes_ranks)

    # Creating the edges (transmission paths)
    for _, row in df_edges.iterrows():
        g.edge(row.From, row.To, arrowhead='vee')

    return g


def view_graph(path_to_transmitters_file:str,
               path_to_transmissions_file:str,
               timeline_step:int, color_origin=dict(), graph_format='pdf', use_example=False) -> None:
    """Displays the final graph (isnad tree) in the given format;
       The following parameters must be provided:
       - a path to the csv file containing the transmitters
       - a path to the csv file containing the transmission
       - the time lapses in years that represent the timeline nodes (timeline_step)
       - the export format: default 'pdf'; others: 'svg', 'png'
       - (optional) a dictionary specifying colors for some or all of
         the origins, or 'auto' for automatic color assignment
    """
    if use_example: # render example graph
        path_to_transmitters_file = 'isnalyser/example_data/trasmitters_example.csv'
        path_to_transmissions_file = 'isnalyser/example_data/transmissions_example.csv'

    g = draw_graph(path_to_transmitters_file,
        path_to_transmissions_file,
        timeline_step,
        color_origin=color_origin)
    
    g.format=graph_format

    g.view()