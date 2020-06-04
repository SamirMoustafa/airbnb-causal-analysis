import os
import csv

import networkx as nx
import matplotlib.pyplot as plt
import pylab


def save_to_file(path, dict_saver):
    """
    save logs without caring about overriding on a file or saving logs in memory.

        dict_saver = {}
        dict_saver.update({'train_loss_mean': train_loss_mean})
        dict_saver.update({'test_loss_mean': val_loss_mean})
        save_to_file(file_to_save_path, dict_saver)

    :param path: path to save file in
    :param dict_saver: dict. contains the new records only
    """

    header = list(dict_saver.keys())
    values = list(dict_saver.values())
    write_results_csv(path, header, values)


def write_results_csv(file_name, headers_name, row_data, operation='a'):
    if len(headers_name) != len(row_data):
        raise ValueError('Row data length must match the file header length')
    _write_data = list()

    if not os.path.exists(file_name):
        operation = 'w'
        _write_data.append(headers_name)

    _write_data.append(row_data)

    with open(file_name, operation) as f:
        writer = csv.writer(f)
        _ = [writer.writerow(i) for i in _write_data]


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
