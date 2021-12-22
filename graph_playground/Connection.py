# import time
# from neo4j import GraphDatabase
#
# class Neo4jConnection:
#     def __init__(self, uri, user, pwd):
#         self.__uri = uri
#         self.__user = user
#         self.__pwd = pwd
#         self.__driver = None
#         try:
#             self.__driver = GraphDatabase.driver(self.__uri, auth=(self.__user, self.__pwd))
#         except Exception as e:
#             print("Failed to create the driver:", e)
#
#     def close(self):
#         if self.__driver is not None:
#             self.__driver.close()
#
#     def query(self, query, parameters=None, db=None):
#         assert self.__driver is not None, "Driver not initialized!"
#         session = None
#         response = None
#         try:
#             session = self.__driver.session(database=db) if db is not None else self.__driver.session()
#             response = list(session.run(query, parameters))
#         except Exception as e:
#             print("Query failed:", e)
#         finally:
#             if session is not None:
#                 session.close()
#         return response
#
#     def add_categories(self, categories):
#         # Adds category nodes to the Neo4j graph.
#         query = '''
#                 UNWIND $rows AS row
#                 MERGE (c:Category {category: row.category})
#                 RETURN count(*) as total
#                 '''
#         ret_val = self.query(query, parameters={'rows': categories.to_dict('records')})
#         return ret_val
#
#     def add_authors(self, rows, batch_size=10000):
#         # Adds author nodes to the Neo4j graph as a batch job.
#         # UNWIND command takes each entity of the list and adds it to the database
#         query = '''
#                 UNWIND $rows AS row
#                 MERGE (:Author {name: row.author})
#                 RETURN count(*) as total
#                 '''
#         ret_val = self.insert_data(query, rows, batch_size)
#         return ret_val
#
#     def insert_data(self, query, rows, batch_size=10000):
#         # Function to handle the updating the Neo4j database in batch mode.
#
#         total = 0
#         batch = 0
#         start = time.time()
#         result = None
#
#         while batch * batch_size < len(rows):
#             res = self.query(query,
#                              parameters={'rows': rows[batch * batch_size:(batch + 1) * batch_size].to_dict('records')})
#             total += res[0]['total']
#             batch += 1
#             result = {"total": total,
#                       "batches": batch,
#                       "time": time.time() - start}
#             print(result)
#
#         return result
#
#     def add_papers(self, rows, batch_size=5000):
#         # Adds paper nodes and (:Author)--(:Paper) and
#         # (:Paper)--(:Category) relationships to the Neo4j graph as a
#         # batch job.
#
#         query = '''
#        UNWIND $rows as row
#        MERGE (p:Paper {id:row.id}) ON CREATE SET p.title = row.title
#
#        // connect categories
#        WITH row, p
#        UNWIND row.category_list AS category_name
#        MATCH (c:Category {category: category_name})
#        MERGE (p)-[:IN_CATEGORY]->(c)
#
#        // connect authors
#        WITH distinct row, p // reduce cardinality
#        UNWIND row.cleaned_authors_list AS author
#        MATCH (a:Author {name: author})
#        MERGE (a)-[:AUTHORED]->(p)
#        RETURN count(distinct p) as total
#        '''
#
#         ret_val = self.insert_data(query, rows, batch_size)
#         return ret_val