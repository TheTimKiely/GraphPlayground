// A Class definition (a node label in Neo4j)
CREATE (person_class:Class {	uri:'http://neo4j.com/voc/movies#Person',
			label:'Person',
			comment:'Individual involved in the film industry'})

// A DatatypeProperty definition (a property in Neo4j)
CREATE (name_dtp:DatatypeProperty {	uri:'http://neo4j.com/voc/movies#name',
				label:'name',
				comment :'A person's name'}),
(name_dtp)-[:DOMAIN]->(person_class)

// An ObjectProperty definition (a relationship in Neo4j)
CREATE (actedin_op:ObjectProperty { 	uri:'http://neo4j.com/voc/movies#ACTED_IN',
				label:'ACTED_IN',
				comment:'Actor had a role in film'}),
(person_class)<-[:DOMAIN]-(actedin_op)-[:RANGE]->(movie_class)

//Added 3 labels, created 4 nodes, set 9 properties, created 3 relationships, completed after 20 ms.