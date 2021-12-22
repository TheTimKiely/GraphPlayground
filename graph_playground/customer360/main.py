import os

import pandas as pd
from sqlalchemy import create_engine

import graph_playground.local_settings as settings
from graph_playground.connections import get_temp_db_name

class GraphNodeConfig(object):
    def __init__(self, name, file_path, pk, fks):
        self.name = name
        self.file_path = file_path
        self.pk = pk
        self.fks = fks
        self.df = pd.read_csv(file_path)

class GraphEdgeConfig(object):
    def __init__(self, name, file_path, node1, node2):
        self.name = name
        self.file_path = file_path
        self.node1 = node1
        self.node2 = node2
        self.df = pd.read_csv(file_path)

def main():
    acct_node = GraphNodeConfig('account', r'/code/books/graph-book/data/ch4/Accounts.csv', 'acct_id', None)
    cc_node = GraphNodeConfig('credit_card', r'/code/books/graph-book/data/ch4/CreditCards.csv', 'cc_num', None)
    cust_node = GraphNodeConfig('customer', r'/code/books/graph-book/data/ch4/Customers.csv', 'customer_id', None)
    loan_node = GraphNodeConfig('loan', r'/code/books/graph-book/data/ch4/Loans.csv', 'loan_id', None)
    nodes = [acct_node, cc_node, cust_node, loan_node]
    owns_edge = GraphEdgeConfig('owns', r'/code/books/graph-book/data/ch4/owns.csv', cust_node, acct_node)
    owes_edge = GraphEdgeConfig('owes', r'/code/books/graph-book/data/ch4/owes.csv', cust_node, loan_node)
    edges = [owns_edge, owes_edge]

    database_name = get_temp_db_name()
    # dfs = dict()
    # for file in input_files:
    #     file_path, file_name = os.path.split(file)
    #     data_name, ext = os.path.splitext(file_name)
    #     df = pd.read_csv(file)
    #     dfs[data_name] = df

    engine = create_engine(settings.POSTGRES_CONNECTION_STRING)
    with engine.connect() as connection:
        for node in nodes:
            print(f"Creating database: {node.name} columns: {node.df.columns}")
            node.df.to_sql(node.name, connection, if_exists='replace', index=False)
            query = f"ALTER TABLE {node.name} ADD PRIMARY KEY ({node.pk});"
            connection.execute(query)
        for edge in edges:
            print(f"Creating database: {edge.name} columns: {edge.df.columns}")
            edge.df.to_sql(edge.name, connection, if_exists='replace', index=False)
            query = f"ALTER TABLE {edge.name} ADD PRIMARY KEY ({edge.node1.pk}, {edge.node2.pk});"
            connection.execute(query)
            query = f"ALTER TABLE {edge.name} ADD FOREIGN KEY ({edge.node1.pk}) REFERENCES {edge.node1.name}({edge.node1.pk});"
            connection.execute(query)
            query = f"ALTER TABLE {edge.name} ADD FOREIGN KEY ({edge.node2.pk}) REFERENCES {edge.node2.name}({edge.node2.pk});"
            connection.execute(query)

    print("Done")

if __name__ == '__main__':
    main()
