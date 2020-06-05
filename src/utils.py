import os
import csv

import numpy as np

import networkx as nx
import matplotlib.pyplot as plt
import pylab


def calculate_monthly(P, mortgage_rate, num_years):
    n = num_years * 12
    monthly_i = mortgage_rate / 12
    numerator = monthly_i * (1 + monthly_i) ** n
    denominator = ((1 + monthly_i) ** n) - 1
    return P * numerator / denominator


def airbnb_income(price, inflation_rate, num_years):
    total = 0
    for year_number in range(num_years):
        curr_inflation = (1 + inflation_rate) ** year_number
        total += (price * curr_inflation) * 12
    return total


def roi(z_estimate, inflation_rate, mortgage_rate, num_years, rental_price, down_payment_percent):
    down_payment = z_estimate * down_payment_percent
    P = z_estimate * (1 - down_payment_percent)

    incurred_cost = calculate_monthly(P, mortgage_rate, num_years) * 12 * num_years + down_payment

    income = airbnb_income(price=rental_price,
                           inflation_rate=inflation_rate,
                           num_years=num_years)

    return (income - incurred_cost) / incurred_cost


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

            if (key1 is 'roi' or key2 is 'roi') and key1 != key2 and values > threshold//10 or values < -threshold//10:
                G.add_edges_from([(key1, key2)], weight=round(values, 2))

    return G


def plot_graph(G):
    edge_labels = dict([((u, v,), d['weight'])
                        for u, v, d in G.edges(data=True)])

    plt.figure(figsize=(18, 18))
    random_pos = nx.random_layout(G, seed=0)
    pos = nx.spring_layout(G, pos=random_pos)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    nx.draw_networkx(G, pos, node_size=3000)
    pylab.show()


def random_z_estimate(price_col):
    mean = np.mean(price_col) // 10
    std = np.std(price_col)
    return np.random.normal(mean, std, price_col.shape[0])
