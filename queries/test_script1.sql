create (hong_kong:Article {name:"Hong Kong", id:"1"})
create (neolithic:Article {name:"Neolithic", id:"2"})
create (boomerang:Article {name:"Boomerang", id:"3"})
create (kangaroo:Article {name:"Kangaroo", id:"4"})
create (scotland:Article {name:"Scotland", id:"5"})

create (hong_kong)-[:game1]->(neolithic)
create (neolithic)-[:game1]->(boomerang)
create (boomerang)-[:game1]->(kangaroo)
create (scotland)-[:game2]->(neolithic)
create (neolithic)-[:game2]->(boomerang)
create (boomerang)-[:game2]->(kangaroo)

match (hong_kong)-[:game1]->(kangaroo) return hong_kong, kangaroo
