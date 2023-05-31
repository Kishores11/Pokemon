from flask import request, url_for, jsonify

from app import app
from app.models import Pokemon, db
from sqlalchemy import func, inspect, delete
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import SQLAlchemyError, DataError, IntegrityError



@app.route("/", methods=["GET"])
@app.route("/<pokemon_rank>", methods=['GET'])
@app.route("/pokemon/<pokemon_name>", methods=['GET'])
def get_pokemons(pokemon_rank=None, pokemon_name=None):
    try:
        pokemon_data = Pokemon.query

        limit = int(request.args.get("limit", app.config.get("PAGE_LIMIT")))
        page_num = request.args.get("page", 1, type=int)

        if pokemon_rank:
            pokemon_data = pokemon_data.filter(Pokemon.rank == pokemon_rank)
            if pokemon_data.with_entities(func.count()).scalar() == 0:
                return {
                    "success": False,
                    "message": "No such pokemon"
                }, 404

        if pokemon_name:
            pokemon_data = pokemon_data.filter(func.lower(Pokemon.name) == pokemon_name.lower())
            if pokemon_data.with_entities(func.count()).scalar() == 0:
                return {
                    "success": False,
                    "message": "No such pokemon"
                }, 404

        pokemon_data = pokemon_data.paginate(page=page_num, per_page=limit, error_out=False)

        next_page_url = None
        if pokemon_data.has_next:
            next_page_url = url_for('get_pokemons', pokemon_rank=pokemon_rank, pokemon_name=pokemon_name, page=pokemon_data.next_num)

        return {
            "success": True,
            "pokemon_data": pokemon_data.items,
            "currentPage": pokemon_data.page,
            "totalPages": pokemon_data.pages,
            "totalCount": pokemon_data.total,
            "nextPageUrl": next_page_url
        }, 200
    except (SQLAlchemyError, DataError, IntegrityError) as e:
        return {
            "success": False,
            "message": str(e)
        }, 500


@app.route("/", methods=['POST', 'PUT'])
def add_pokemon():
    pokemon_data_list = request.json  # Assuming the data is provided in the request body as a list of JSON objects

    values = []  # List to store the values for bulk insertion

    # Get the column names and default values from the table
    table = Pokemon.__table__
    mapper = inspect(Pokemon)
    column_defaults = {c.name: c.default.arg for c in mapper.columns if c.default is not None}

    for pokemon_data in pokemon_data_list:
        # Retrieve the existing values for missing columns from the table
        existing_values = db.session.query(Pokemon).filter_by(name=pokemon_data['name']).first()

        # Create a dictionary with existing and default values from the table
        pokemon_values = {column: getattr(existing_values, column) if hasattr(existing_values, column) else column_defaults.get(column) for column in table.columns.keys()}


        # Update the dictionary with values from the request, if available
        pokemon_values.update(pokemon_data)

        # Append the Pokemon's data to the values list
        values.append(pokemon_values)

    # Create an insert statement using the upsert command and the bulk values
    insert_statement = insert(Pokemon).values(values)

    on_conflict_statement = insert_statement.on_conflict_do_update(
        constraint='pokemon_pkey',  # Specify the primary key constraint name
        set_=dict(
            rank=insert_statement.excluded.rank,
            type_1=insert_statement.excluded.type_1,
            type_2=insert_statement.excluded.type_2,
            total=insert_statement.excluded.total,
            hp=insert_statement.excluded.hp,
            attack=insert_statement.excluded.attack,
            defence=insert_statement.excluded.defence,
            speed=insert_statement.excluded.speed,
            generation=insert_statement.excluded.generation,
            legendary=insert_statement.excluded.legendary
        )
    )

    try:
        db.session.execute(on_conflict_statement)
        db.session.commit()
        return {
            "success": True,
            "message": "Pokemon added/updated successfully"
        }, 200
    except:
        db.session.rollback()
        return {
            "success": False,
            "message": "Failed to add/update Pokemon"
        }, 500


@app.route("/", methods=["DELETE"])
@app.route("/<pokemon_name>", methods=["DELETE"])
def delete_pokemon(pokemon_name=None):
    if pokemon_name:
        pokemon_names = [pokemon_name]
    else:
        data = request.get_json()
        pokemon_names = data.get("names", [])

    if not pokemon_names:
        return {
            "success": False,
            "message": "No Pokemon names provided",
        }, 400

    deleted_pokemon_names = []
    for name in pokemon_names:
        pokemon = Pokemon.query.filter(func.lower(Pokemon.name) == name.lower()).first()
        if pokemon:
            deleted_pokemon_names.append(pokemon.name)
            db.session.delete(pokemon)

    db.session.commit()

    return {
        "success": True,
        "deleted_pokemon_names": deleted_pokemon_names,
        "message": f"Deleted Pokemons with names: {deleted_pokemon_names}",
    }


@app.route("/legendary-pokemons", methods=['GET'])
def get_legendary_pokemons():
    try:
        legendary_pokemons = Pokemon.query.filter(Pokemon.legendary == "true").all()

        pokemon_list = []
        for pokemon in legendary_pokemons:
            pokemon_data = {
                "name": pokemon.name,
                "rank": pokemon.rank,
            }
            pokemon_list.append(pokemon_data)

        return jsonify({
            "success": True,
            "legendary_pokemons": pokemon_list
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500
    

@app.route("/generation-pokemons/<generation_number>", methods=['GET'])
def get_generation_pokemons(generation_number=None):
    try:
        if generation_number is None:
            return jsonify({
                "success": False,
                "message": "Generation parameter is required."
            }), 400

        generation_pokemons = Pokemon.query.filter(Pokemon.generation == generation_number).all()

        pokemon_list = []
        for pokemon in generation_pokemons:
            pokemon_data = {
                "name": pokemon.name,
                "rank": pokemon.rank,
            }
            pokemon_list.append(pokemon_data)

        return jsonify({
            "success": True,
            f"pokemons of generation number {generation_number}": pokemon_list
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500
