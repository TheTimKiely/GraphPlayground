import datetime as dt

import graph_playground.local_settings as settings
from datastore_connector.neo4j_connection import Neo4jConnection
from datastore_connector.stardog_connection import StardogConnection


def get_temp_db_name():
    now = dt.datetime.now()
    ret_val = f'TestDb_{now.month}{now.day}{now.year}'
    return ret_val

def get_neo_connection():
    ret_val = Neo4jConnection(settings.NEO4J_URI, settings.NEO4J_USER, settings.NEO4J_PASSWORD)
    return ret_val

def create_neo_database(database_name):
    # Neo4j Community Edition does not support multiple database, so just clear existing
    database_name = 'neo4j'
    query = """MATCH (n)
                DETACH DELETE n"""
    connection = Neo4jConnection(settings.NEO4J_URI, settings.NEO4J_USER, settings.NEO4J_PASSWORD)
    # result = connection.create_database(database_name)
    result = connection.query(database_name, query)

def get_stardog_connection():
    ret_val = StardogConnection(settings.STARDOG_URI, settings.STARDOG_USER, settings.STARDOG_PASSWORD)
    return ret_val

def create_stardog_database(name):
    connection = StardogConnection(settings.STARDOG_URI, settings.STARDOG_USER, settings.STARDOG_PASSWORD)
    db = connection.create_database(name, drop=True)
    print(db)
