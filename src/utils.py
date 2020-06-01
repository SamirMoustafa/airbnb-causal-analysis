import networkx as nx
import matplotlib.pyplot as plt
import pylab


def df2graph(df, threshold):
    G = nx.DiGraph()

    for key1 in df:
        for j, values in enumerate(df[key1]):
            key2 = df.columns[j]
            if key1 != key2 and values > threshold or values < -threshold:
                G.add_edges_from([(key1, key2)], weight=round(values, 2))
    return G


def plot_graph(G):
    edge_labels = dict([((u, v,), d['weight'])
                        for u, v, d in G.edges(data=True)])

    plt.figure(figsize=(18, 18))
    random_pos = nx.random_layout(G, seed=0)
    pos = nx.spring_layout(G, pos=random_pos)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    nx.draw_networkx(G, pos, node_size=3000, with_label=True)
    pylab.show()