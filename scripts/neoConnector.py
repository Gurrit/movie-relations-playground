from neo4j import GraphDatabase
from dataExtractor import parse_movies_from_file

class NeoConnector:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()


def insert_movie(connector, movie):
    movie_insert_query = "MERGE (m:Movie {id: $id, name: $movieName}) RETURN m.name as name"
    print("inserting {}".format(movie.name))
    records, summary, keys = connector.driver.execute_query(
        movie_insert_query,
        parameters_ = { "movieName": movie.name, "id": movie.id },
        database_ = "neo4j"
    )
    for actor in movie.actors:
        actors_insert_query = ("MATCH (m:Movie {id: $movieId})"
                             "MERGE (a:Actor {name: $actorName, id: $actorId}) " +
                             "MERGE (a)-[:ACTED_IN {creditOrder: $creditOrder, character: $character}]->(m)" +
                             "RETURN a.name as name")
        records, summary, keys = connector.driver.execute_query(
            actors_insert_query,
            parameters_= {
                "movieId": movie.id,
                "actorName": actor.name,
                "actorId": actor.id,
                "creditOrder": actor.credit_order,
                "character": actor.character
            },
            database_="neo4j"
        )


if __name__ == "__main__":
    movies = parse_movies_from_file("../tmdb_5000_credits.csv")
    connector = NeoConnector("bolt://localhost:7687", "neo4j", "password")
    list(map(lambda movie: insert_movie(connector, movie), movies))


#MATCH
#(KevinB:Actor {name: 'Kevin Bacon'}),
#(Al:Actor {name: 'Ethan Hawke'}),
#p = shortestPath((KevinB)-[:ACTED_IN*]-(Al))
#WHERE all(r IN relationships(p) WHERE r IS NOT NULL)
#RETURN p