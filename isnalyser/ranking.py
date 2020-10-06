"""This module contains 3 functions
   <rank_list> attributes to each node a rank according to its death date
   <same_rank_subgraph> matches the nodes of the subgraph, i.e the dates, with the corresponding node of the main graph, i.e. the transmitters
   <a_timeline> creates the a subgraph with the dates
"""

def rank_list(date, rank, df):
    """
    Return a list with the date and all the node 
    ids that should be placed at the same rank.
    """
    raise NotImplementedError


def same_rank_subgraph(G, rank_lst):
    """
    Return subgraph of nodes from same-rank ids.
    """
    raise NotImplementedError


def a_timeline(G, minimum, maximum, step, n_attr, e_attr):
    """
    creates a timeline in the form of a subgraph
    G = the original graph
    s = G's subgraph
    minimum = start of the timeline
    maximum = end of the timeline
    step = years' slice
    n_attr = dict with the attribute of the subgraph's nodes
    e_attr = dict with the attribute of the subgraph's edges
    """
    raise NotImplementedError
