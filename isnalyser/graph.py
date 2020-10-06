"""The <graph> module draws the final graph creating 
and connecting all the nodes together with edges 
and aligning them to the timeline subgraph."""

def draw_graph():
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
    raise NotImplementedError