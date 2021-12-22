import os

import numpy as np
import pandas as pd
from graph_playground.connections import get_temp_db_name, get_neo_connection, get_stardog_connection

def run_sundog_ingest(input_files):
    conn = get_stardog_connection()
    database_name = get_temp_db_name()
    conn.create_database(database_name, drop=True)
    conn.load_data(database_name, input_files)
    query = """
    SELECT ?date WHERE {
      ?s a <http://stardog.com/tutorial/Album> ;
        <http://stardog.com/tutorial/date> ?date .
    }
    """
    result = conn.query(database_name, query)
    df = pd.read_csv(io.BytesIO(csv_results))
    df.head()

def main():
    base_dir = os.path.dirname(__file__)
    data_dir = os.path.join(base_dir, 'data')
    input_files = [os.path.join(data_dir, 'music_schema.ttl'), os.path.join(data_dir, 'music.ttl.gz')]
    run_sundog_ingest(input_files)
    # neo_ingest(input_files)
    print('Done')

if __name__ == '__main__':
    main()