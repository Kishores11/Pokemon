import os
import sys
import requests
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import insert

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(parentdir)
sys.path.insert(0, parentdir)

from app import app
from app.models import Pokemon, db


def create_object_in_db_at_startup():
    # Read the data from load.json
    response = requests.get('https://coralvanda.github.io/pokemon_data.json')
    data = response.json()


    # Iterate over the Question objects and insert them into the database
    for pokemon_data in data:
        pokemon = Pokemon(
                rank=pokemon_data["#"],
                name=pokemon_data["Name"],
                type_1=pokemon_data["Type 1"],
                type_2=pokemon_data["Type 2"],
                total=pokemon_data["Total"],
                hp=pokemon_data["HP"],
                attack=pokemon_data["Attack"],
                defence=pokemon_data["Defense"],
                speed=pokemon_data["Speed"],
                generation=pokemon_data["Generation"],
                legendary=pokemon_data["Legendary"]
            )
        db.session.add(pokemon)

    # Commit the changes to the database
    db.session.commit()

    print("Data loaded successfully")


create_object_in_db_at_startup()