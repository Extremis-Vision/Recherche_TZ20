from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "testyudsqdqs23"))

with driver.session() as session:
    result = session.run("RETURN 1 AS test")
    print(result.single())
