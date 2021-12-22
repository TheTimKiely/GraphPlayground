import json
import os

from tqdm import tqdm

import pandas as pd

from graph_playground.Connection import Neo4jConnection

pd.set_option('display.width', 400)
pd.set_option('display.max_columns', 10)

import matplotlib.pyplot as plt

import networkx as nx

def init_graph(conn):
    conn.query('CREATE CONSTRAINT papers IF NOT EXISTS ON (p:Paper)     ASSERT p.id IS UNIQUE')
    conn.query('CREATE CONSTRAINT authors IF NOT EXISTS ON (a:Author) ASSERT a.name IS UNIQUE')
    conn.query('CREATE CONSTRAINT categories IF NOT EXISTS ON (c:Category) ASSERT c.category IS UNIQUE')


def prepare_data(df):
    def get_author_list(line):
        # Cleans author dataframe column, creating a list of authors in the row.
        return [e[1] + ' ' + e[0] for e in line]

    def get_category_list(line):
        # Cleans category dataframe column, creating a list of categories in the row.
        return list(line.split(" "))

    df['cleaned_authors_list'] = df['authors_parsed'].map(get_author_list)
    df['category_list'] = df['categories'].map(get_category_list)
    df = df.drop(['submitter', 'authors',
                  'comments', 'journal-ref',
                  'doi', 'report-no', 'license',
                  'versions', 'update_date',
                  'abstract', 'authors_parsed',
                  'categories'], axis=1)
    return df


def main(input_file):
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

    df = prepare_data(df)

    categories = pd.DataFrame(df[['category_list']])
    categories.rename(columns={'category_list': 'category'},
                      inplace=True)
    categories = categories.explode('category') \
        .drop_duplicates(subset=['category'])

    authors = pd.DataFrame(df[['cleaned_authors_list']])
    authors.rename(columns={'cleaned_authors_list': 'author'},
                   inplace=True)
    authors = authors.explode('author').drop_duplicates(subset=['author'])


    conn = Neo4jConnection(uri="bolt://wakhanthanka:7687",
                           user="neo4j",
                           pwd="test")

    init_graph(conn)

    conn.add_categories(categories)
    conn.add_authors(authors)
    conn.add_papers(df)


print('Done')


if __name__ == '__main__':
    input_file = 'data/jira_sample.csv'
    # input_file = 'data/arxiv-metadata-oai-snapshot.json'
    main(input_file)