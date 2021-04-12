from api import app
from api.routes import Pokemons, Encounters  # This import is needed to attach routes to the app
from api.utils import create_logger

if __name__ == '__main__':
    create_logger('PokemonAPI')
    app.run(debug=True)
