r"""
The <graph> module draws the final graph creating 
and connecting all the nodes together with edges 
and aligning them to the timeline subgraph.
"""

from collections import defaultdict
import itertools
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from graphviz import Digraph

from pkg_resources import resource_filename

from isnalyser.ranking import rank_list, same_rank_subgraph, a_timeline
from isnalyser.colors import get_discrete_cmap
from isnalyser.paths import path_all, merge_edges


def draw_graph(path_to_transmitters_file:str,
               path_to_transmissions_file:str,
               timeline_step:int, 
               color_origin='auto',
               edge_label=True) -> Digraph:
    """
    Draw the final graph by
    (1) creating a dataframe with nodes (transmitters) using the
    database_to_dataframe function;
    (2) creating the edges (transmission path) using the
    database_to_dataframe function, adding labels from the Variant column;
    (3) ranking the nodes to match them with the timeline subgraph;
    (4) creating the graph as <g>;
    (5) creating the nodes within <g>;
    (6) defining the timeline subgraph attributes;
    (7) creating the timeline subgraph with a_timeline function;
    (8) linking the nodes of the subgraph and the main graph together
        with the functions rank_list and same_rank_subgraph;
    (9) drawing the edges.
    The output is a graph in pdf, svg or png format. Default is pdf.
    """
    assert path_to_transmissions_file.endswith('.csv') and\
           path_to_transmitters_file.endswith('.csv'), "Please provide .csv input files."

    # Initiate the dataframes from input files
    df_nodes = pd.read_csv(path_to_transmitters_file, 
                           header=0, 
                           names=['Transmitter','dAH','Origin'], # column names are used in the code
                           index_col=False, 
                           skipinitialspace=True) # prevent extra white space around the separator
    # Load data from file and process
    df_edges = pd.read_csv(path_to_transmissions_file, 
                           header=0, 
                           names=['From','To','Variant'], # the column names cannot be changed
                           index_col=False, 
                           skipinitialspace=True) # prevent extra white space around the separator
    df_edges = merge_edges(df_edges)
    # Create ranking ids
    df_nodes['Ranking'] = df_nodes.dAH // timeline_step



    # Create the main graph    
    g = Digraph('graph', filename='graph.gv',
                graph_attr=dict(size='8,11', fontsize='16',
                ranksep='1.2', concentrate='false'),
                node_attr=dict(shape='none'))
    

    # Color nodes according to origin
    num_origins = df_nodes.Origin.nunique(dropna=False)
    if color_origin == 'auto':
        cmap = get_discrete_cmap(num_origins, base_cmap='nipy_spectral')
        colors = (mpl.colors.to_hex(cmap(i)) for i in range(num_origins))
        color_cycle = itertools.cycle(colors)
        # Attribute colors to geographical origins
        color_origin = dict()
        for i, origin in enumerate(df_nodes.Origin.unique()):
            color_origin[origin] = next(color_cycle)
    else:
        # Set all origins as black except those in the color_origin parameter
        color_origin = defaultdict(lambda: 'black', color_origin)

    df_nodes['Color'] = df_nodes.Origin.map(color_origin)
    

    # Create the nodes
    for _, row in df_nodes.iterrows():
        g.node(name=row.Transmitter, fontcolor=row.Color, fontsize='20', fontname='DejaVu Serif')

    # Define the timeline subgraph attributes
    minimum = df_nodes.Ranking.min()
    maximum = df_nodes.Ranking.max()

    # Create a dictionary of nodes' attributes
    n_attr = {'name':'j', 'shape':'none', 'fontsize':'15.0', 'fontname':'Calibri'}

    # Create a dictionary of edges' attributes
    e_attr = {'arrowhead':'none', 'color':'black', 'penwidth':'2', 'len':'1.0'}

    # Create the timeline as a subgraph
    a_timeline(g, minimum*timeline_step, maximum*timeline_step, timeline_step, n_attr, e_attr)

    # Link the nodes of the subgraph and the main graph together
    for rank in range(df_nodes.Ranking.unique().max()+1):
        nodes_ranks = rank_list(str(rank*timeline_step), rank, df_nodes)
        same_rank_subgraph(g, nodes_ranks)

    # Create the edges (transmission paths)
    for _, row in df_edges.iterrows():
        if edge_label:
            attributes = {'xlabel':row.paths, 'arrowhead':'vee', 'fontcolor':'#AC9393', 'fontsize':'16.0', 'fontname':'Calibri'}
            g.edge(row.From, row.To, **attributes)
        else:
            g.edge(row.From, row.To, arrowhead='vee')

    # Add a legend
    mid_legend_node = int(num_origins/2) # Set midpoint... this will be connected to main graphs top node
    legend_nodes = []
    with g.subgraph() as l: # Init legend as new subgraph
        l.attr(rankdir='LR')
        for i, o in enumerate(df_nodes.Origin.unique()): # add nodes
            if o in color_origin.keys() and type(o)==str:
                l.node(name=o, shape='ellipse', color=color_origin[o], fontname='DejaVu Serif', fontsize='20.0')
                l.attr(rank='min')
                legend_nodes.append(o)
                if i==mid_legend_node: # if legend node is midpoint, place it over the main graphs top node
                    g.edge(o, df_nodes.loc[df_nodes.dAH == df_nodes.dAH.min()].Transmitter.values[0], color='white')
        
        # Add (invisible) connections so that they are ordered and actually midpoint is above top node
        for j in range(1, len(legend_nodes)):
            l.edge(legend_nodes[j-1], legend_nodes[j], color='white')


    return g


def view_graph(path_to_transmitters_file:str,
               path_to_transmissions_file:str,
               timeline_step:int, 
               color_origin='auto', 
               graph_format='svg', 
               use_example=False,
               edge_label=True) -> None:
    """Display the final graph (isnad tree) in the given format;
       The following parameters must be provided:
       - a path to the csv file containing the transmitters
       - a path to the csv file containing the transmission
       - the time lapses in years that represent the timeline nodes (timeline_step)
       - the export format: default 'svg'; others: 'pdf', 'png'
       - (optional) a dictionary specifying colors for some or all of
         the origins, or 'auto' for automatic color assignment
       - (optional) edge_label=False to remove the labels on edges.
    """
    if use_example: # Render example graph
        path_to_transmitters_file = resource_filename(__name__, 'example_data/transmitters_example.csv')
        path_to_transmissions_file = resource_filename(__name__, 'example_data/transmissions_example.csv')

    g = draw_graph(path_to_transmitters_file,
        path_to_transmissions_file,
        timeline_step,
        color_origin=color_origin,
        edge_label=edge_label)
    
    g.format=graph_format

    g.view()
