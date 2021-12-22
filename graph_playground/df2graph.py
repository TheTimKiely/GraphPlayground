import json
import os

from tqdm import tqdm

import pandas as pd

from graph_playground.Connection import Neo4jConnection

pd.set_option('display.width', 400)
pd.set_option('display.max_columns', 10)

import matplotlib.pyplot as plt

import networkx as nx

class Node():
    def __init__(self, name):
        self.name = name

def main(input_file):

    g = nx.Graph()
    n1 = Node('one')
    g.add_node(n1)
    n2 = Node('two')
    g.add_node(n2)
    e1 = g.add_edge(n1, n2)

    plt.figure(figsize=(10, 8))
    nx.draw_shell(g, with_labels=True)


    ext = os.path.splitext(input_file)[1]
    if ext == '.csv':
        df = pd.read_csv(input_file)
    elif ext == '.json':
        metadata = []

        lines = 100000  # 100k for testing
        with open(input_file, 'r') as f:
            for line in tqdm(f):
                metadata.append(json.loads(line))
                lines -= 1
                if lines == 0: break

        df = pd.DataFrame(metadata)
    else:
        raise Exception(f'Unsupported extension: {ext}')

    G = nx.Graph()
    G = nx.from_pandas_edgelist(df, 'Assignee', 'Reporter')

    plt.figure(figsize=(10, 8))
    nx.draw_shell(G, with_labels=True)

    print('Done')


if __name__ == '__main__':
    input_file = 'data/jira_sample.csv'
    main(input_file)