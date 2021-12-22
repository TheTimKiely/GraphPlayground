import os
import time

import numpy as np
import pandas as pd
from neo4j import basic_auth, GraphDatabase

pd.set_option('display.width', 400)
pd.set_option('display.max_columns', 10)

import matplotlib.pyplot as plt

# from py2neo import Graph, Schema

import graph_playground.local_settings as settings


def py2neo_graph_structure():
    from py2neo import Graph, Node, Relationship
    gdb = Graph(user=settings.NEO4J_USER, password =settings.NEO4J_PASSWORD)
    # Get Distinct Node Labels
    NodeLabel = list(gdb.schema.node_labels)
    print(NodeLabel)
    # For each node type print attributes
    Node = []
    Attr = []
    for nl in NodeLabel:
        for i in gdb.schema.get_indexes(nl):
            Node.append(nl)
            Attr.append(format(i))
    NodeLabelAttribute = pd.DataFrame(
        {'NodeLabel': Node, 'Attribute': Attr})
    print(NodeLabelAttribute.head(5))


def neo_graph_structure():
    # from neo4j.v1 import GraphDatabase, basic_auth
    driver = GraphDatabase.driver('bolt: // localhost: 7687', auth = basic_auth(settings.NEO4J_USER, settings.NEO4J_PASSWORD))
    sess = driver.session()
    q = '''MATCH(n)  RETURN distinct labels(n)'''
    res = sess.run(q)
    NodeLabel = []
    for r in res:
        temp = r['labels(n)']
        if temp != '':
            NodeLabel.extend(temp)
    NodeLabel = list(filter(None, NodeLabel))
    # For each node label print attributes
    Node, Attr = ([] for i in range(2))
    for nl in NodeLabel:
        q = 'MATCH(n:' + str(nl) + ')\n' + 'RETURN distinct keys(n)'
        res = sess.run(q)
        temp = []
        for r in res:
            temp.extend(r['keys(n)'])
            temp2 = list(set(temp))
            Attr.extend(temp2)
            for i in range(len(temp2)):
                Node.append(nl)
        NodeLabelAttribute = pd.DataFrame(
            {'NodeLabel': Node, 'Attribute': Attr})
        print(NodeLabelAttribute.head(5))

def query_graph_structure():
    py2neo_graph_structure()
    # neo_graph_structure()

def main():
    query_graph_structure()
    print('Done')


if __name__ == '__main__':
    main()
