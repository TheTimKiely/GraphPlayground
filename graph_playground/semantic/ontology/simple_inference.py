import os
from shutil import copyfile

import time

import datetime as dt

import numpy as np
import pandas as pd

from datastore_connector.neo4j_connection import Neo4jConnection
from datastore_connector.stardog_connection import StardogConnection

pd.set_option('display.width', 400)
pd.set_option('display.max_columns', 10)

import matplotlib.pyplot as plt

import graph_playground.local_settings as settings



def load_stardog_data(database_name, data_files):
    connection = StardogConnection(settings.STARDOG_URI, settings.STARDOG_USER, settings.STARDOG_PASSWORD)
    result = connection.load_data(database_name, data_files)


def query_data(database_name, connection):
    simple_query = r"""
    PREFIX ab: <http://learningsparql.com/ns/addressbook#>     
    select ?firstName ?lastName 
    WHERE 
    {
      ?person ab:region 'Connecticut' ;
              ab:firstName ?firstName ;
              ab:lastName ?lastName . 
    }"""
    inference_query = r"""
    PREFIX ab: <http://learningsparql.com/ns/addressbook#> 
    select ?firstName ?lastName 
    WHERE 
    {
      ?person a ab:Musician ;
              ab:firstName ?firstName ;
              ab:lastName ?lastName . 
    }"""
    simple_result = connection.query(database_name, simple_query)
    print(simple_result)
    inference_result = connection.query(database_name, inference_query, reasoning=True)
    print(inference_result)


def query_stardog_data(database_name):
    connection = StardogConnection(settings.STARDOG_URI, settings.STARDOG_USER, settings.STARDOG_PASSWORD)
    query_data(database_name, connection)


    print(result)


def load_neo_data(database_name, data_files):

    # Neo4j is running in a Docker container, so copy files to the mounted volume
    docker_data_files = []
    for data_file in data_files:
        file_path, file_name = os.path.split(data_file)
        docker_volume = r'/home/tim/neo4j/logs'
        dest_path = os.path.join(docker_volume, file_name)
        copyfile(data_file, dest_path)
        docker_data_files.append(os.path.join('/logs', file_name))
    data_files = docker_data_files

    # Neo4j Community Edition does not support multiple database, so just clear existing
    database_name = 'neo4j'
    connection = Neo4jConnection(settings.NEO4J_URI, settings.NEO4J_USER, settings.NEO4J_PASSWORD)
    result = connection.load_data(database_name, data_files)
    return result


def query_neo_data(database_name, data_files):
    # Neo4j Community Edition does not support multiple database, so just clear existing
    database_name = 'neo4j'
    connection = Neo4jConnection(settings.NEO4J_URI, settings.NEO4J_USER, settings.NEO4J_PASSWORD)
    query_data(database_name, connection)


def main():

    create = True
    run_stardog = False
    run_neo = True
    database_name = get_temp_db_name()
    base_dir = os.path.dirname(__file__)
    data_dir = os.path.join(base_dir, 'data')
    data_files = [os.path.join(data_dir, 'musician.ttl'), os.path.join(data_dir, 'instrument_player.ttl'),
                  os.path.join(data_dir, 'richard.ttl')]

    if run_stardog:
        if create:
            create_stardog_database(database_name)
            load_stardog_data(database_name, data_files)
        query_stardog_data(database_name)

    if run_neo:
        if create:
            create_neo_database(database_name)
            load_neo_data(database_name, data_files)
    query_neo_data(database_name, data_files)
    print('Done')


if __name__ == '__main__':
    main()