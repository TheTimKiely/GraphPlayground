
import os

import rdflib
from rdflib import Graph, Namespace, RDF, RDFS, BNode, URIRef, Literal


#
# from owlready2 import *
# from owlready2.pymedtermino2.umls import *


class Person(object):
    def __init__(self, first_name):
        self.first_name = first_name

class Musician(Person):
    def __init__(self, name):
        super(Musician, self).__init__(name)
        self.namespace = 'http://com.tim.semantic'

    def to_rdf(self, graph):
        """
S: http://learningsparql.com/ns/addressbook#MusicalInstrument, 	P: http://www.w3.org/1999/02/22-rdf-syntax-ns#type, 	O: http://www.w3.org/2000/01/rdf-schema#Class
S: http://learningsparql.com/ns/addressbook#Musician, 	P: http://www.w3.org/1999/02/22-rdf-syntax-ns#type, 	O: http://www.w3.org/2000/01/rdf-schema#Class
S: http://learningsparql.com/ns/addressbook#MusicalInstrument, 	P: http://www.w3.org/2000/01/rdf-schema#label, 	O: musical instrument
S: http://learningsparql.com/ns/addressbook#Musician, 	P: http://www.w3.org/2000/01/rdf-schema#label, 	O: Musician
S: http://learningsparql.com/ns/addressbook#Musician, 	P: http://www.w3.org/2000/01/rdf-schema#comment, 	O: Someone who plays a musical instrument
        """
        n_ab = Namespace('http://learningsparql.com/ns/addressbook#')
        n_rdf = Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
        n_ab = Namespace('http://www.w3.org/2000/01/rdf-schema#')

        # musician = BNode()
        musician = URIRef('http://learningsparql.com/ns/addressbook#Musician')
        graph.bind('ab', 'http://learningsparql.com/ns/addressbook#')
        graph.add((musician, RDF.type, RDFS.Class))
        graph.add((musician, RDFS.label, Literal('Musician')))
        return graph


def print_graph(rdf_url):
    g = Graph()
    g.parse(rdf_url)

    for s, p, o in g:
        print(f'S: {s}, \tP: {p}, \tO: {o}')

def main():
    rdf_url = 'http://dbpedia.org/resource/Semantic_Web'
    rdf_url = r'/code/samples/semantic/learningSparql/musician.ttl'
    # rdf_url = r'/code/samples/semantic/learningSparql/instrument_player.ttl'
    # print_graph(rdf_url)

    m = Musician('Bob')
    g = Graph()
    m.to_rdf(g)
    g.serialize('data/test/bob.ttl')


if __name__ == '__main__':
    main()