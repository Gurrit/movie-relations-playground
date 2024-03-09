import json
import csv

class Actor:
    def __init__(self, id, name, character, credit_order):
        self.id = id
        self.name = name
        self.character = character
        self.credit_order = credit_order


class Movie:
    def __init__(self, id, name, actors):
        self.id = id
        self.name = name,
        self.actors = actors



def parse_movie(id, movieName, actorsJsonStr):
    actorsJson = json.loads(actorsJsonStr)
    actors = map(lambda actor: Actor(id = actor["id"], name = actor["name"], character = actor["character"], credit_order = actor["order"]), actorsJson)
    return Movie(id, movieName, actors)


def parse_movies_from_file(fileName):
    with open(fileName, 'r') as file:
        reader = csv.DictReader(file)
        return list(map(lambda row: parse_movie(row["movie_id"], row["title"], row["cast"]), reader))


# This File assumes that the format of the input is the same as This dataset:
# https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata.