from api import db


class Sprite(db.EmbeddedDocument):
    back_default = db.URLField(null=True)
    back_female = db.URLField(null=True)
    back_shiny = db.URLField(null=True)
    back_shiny_female = db.URLField(null=True)
    front_default = db.URLField(null=True)
    front_female = db.URLField(null=True)
    front_shiny = db.URLField(null=True)
    front_shiny_female = db.URLField(null=True)

    @classmethod
    def pick_specified_fields(cls, sprite_dict):
        """
        Filter dictionary fetched from pokemon API using specified Sprite fields.
        """
        return {sprite: sprite_url for sprite, sprite_url in sprite_dict.items() if sprite in cls._fields}


class Pokemon(db.Document):
    base_experience = db.IntField(required=True)
    height = db.IntField(required=True)
    id = db.IntField(db_field='id', primary_key=True)
    name = db.StringField(unique=True, required=True)
    sprites = db.EmbeddedDocumentField(Sprite)
    weight = db.IntField(required=True)


"""
Example Pokemon:

{
  "base_experience": 64,
  "height": 7,
  "id": 1,
  "name": "bulbasaur",
  "sprites": {
    "back_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/1.png",
    "back_female": null,
    "back_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/shiny/1.png",
    "back_shiny_female": null,
    "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png",
    "front_female": null,
    "front_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/1.png",
    "front_shiny_female": null
  },
  "weight": 69
}

"""
