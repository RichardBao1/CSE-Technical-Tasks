from dataclasses import dataclass
from enum import Enum
from typing import Union, NamedTuple, List
from flask import Flask, request, jsonify
from math import dist


# SpaceCowboy models a cowboy in our super amazing system
@dataclass
class SpaceCowboy:
    name: str
    lassoLength: int


# SpaceAnimal models a single animal in our amazing system
@dataclass
class SpaceAnimal:
    # SpaceAnimalType is an enum of all possible space animals we may encounter
    class SpaceAnimalType(Enum):
        PIG = "pig"
        COW = "cow"
        FLYING_BURGER = "flying_burger"

    type: SpaceAnimalType


# SpaceEntity models an entity in the super amazing (ROUND UPPER 100) system
@dataclass
class SpaceEntity:
    class Location(NamedTuple):
        x: int
        y: int

    metadata: Union[SpaceCowboy, SpaceAnimal]
    location: Location


# ==== HTTP Endpoint Stubs ====
app = Flask(__name__)
space_database: List[SpaceEntity] = []


# the POST /entity endpoint adds an entity to your global space database
@app.route('/entity', methods=['POST'])
def create_entity():
    """ parses space animals and space cowboys to database"""
    try:
        # collects json from post request
        json = request.get_json()

        # loop
        for entity in json['entities']:
            x_coord = entity["location"]["x"]
            y_coord = entity["location"]["y"]
            loc = SpaceEntity.Location(x_coord, y_coord)

            if entity["type"] == "space_animal":
                animal_type = SpaceAnimal.SpaceAnimalType(entity["metadata"]["type"])
                space_animal = SpaceAnimal(type=animal_type)
                space_entity = SpaceEntity(metadata=space_animal, location=loc)
            elif entity["type"] == "space_cowboy":
                space_cowboy = SpaceCowboy(name=entity["metadata"]["name"],
                                           lassoLength=entity["metadata"]["lassoLength"])
                space_entity = SpaceEntity(metadata=space_cowboy, location=loc)
            else:
                raise KeyError("Wrong entity type inputted")

            space_database.append(space_entity)

        # return status code 200 if successful
        return "", 200

    except Exception as e:
        # return status code 400 if not successful
        return "", 400


# lassoable returns all the space animals a space cowboy can lasso given their name
@app.route('/lassoable', methods=['GET'])
def lassoable():
    """ finds all space animals that the lasso can catch for a given cowboy """

    try:
        output = {"space_animals": []}

        cowboy = request.get_json()["cowboy_name"]

        for entity in space_database:
            if isinstance(entity.metadata, SpaceCowboy) and entity.metadata.name == cowboy:
                lasso_length = entity.metadata.lassoLength
                loc = entity.location
                break

        for entity in space_database:
            if isinstance(entity.metadata, SpaceAnimal) and distance(loc.x, loc.y, entity.location.x,
                                                                     entity.location.y) <= lasso_length:
                output["space_animals"].append(entity_format_output(entity))

        return jsonify(output), 200

    except Exception as e:
        # return status code 400 if not successful
        print(e)
        return "", 400


def distance(p_x, p_y, q_x, q_y) -> float:
    """ calculates pythagorean distance between two points p and q """

    return ((p_x - q_x) ** 2 + (p_y - q_y) ** 2) ** 0.5


def entity_format_output(entity) -> dict:
    """ reformats entity into appropriate json output """

    entity_output = {"type": entity.metadata.type.value, "location": {"x": entity.location.x, "y": entity.location.y}}
    return entity_output


# DO NOT TOUCH ME, thanks :D
if __name__ == '__main__':
    app.run(debug=True, port=8080)
