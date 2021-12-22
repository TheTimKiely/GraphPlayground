CREATE (p:Person {firstName: 'Richard', lastName: "Mutt",
        postalCode: "49345", city: "Springfield", homeTel: "(229) 276-5135", streetAddress: "32 Main St.",
        region: "Connecticut", email: "richard49@hotmail.com"})
CREATE (v:MusicalInstrument {name:'vacuumCleaner'})
CREATE (p)--[r:PlaysInstrument]->(v)
