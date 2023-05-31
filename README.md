In this application the pokemon data is fetched from a link 'https://coralvanda.github.io/pokemon_data.json'
and then added into the database. For this I created a python file called load_initial_data.py. When we run
this file it initially load our database with the pokemons present in the link.

The routes created are:
1)(GET)http://127.0.0.1:5000/ - this will give all the pokemon details.
2)(GET)http://127.0.0.1:5000/<pokemon_rank> - this will give the pokemon having the specified rank.
3)(GET)http://127.0.0.1:5000/pokemon/<pokemon_name> - this will give the pokemon having the specified name.
4)(POST,PUT)http://127.0.0.1:5000/ - this will add a new pokemon if is not present in the database, on conflict  with thepokemon name it will update that row.
5)(DELETE)http://127.0.0.1:5000/ - this will delete the given pokemon name(here the pokemon name is passed in body part.
6)(DELETE)http://127.0.0.1:5000/<pokemon_name> - this will delete the given pokemon name.
7)(GET)http://127.0.0.1:5000/legendary-pokemons - this will give the list of legendary pokemons.
8)(GET)http://127.0.0.1:5000/generation-pokemons/<generation_number> - this will give the list of pokemons having the passed generation number in the url.