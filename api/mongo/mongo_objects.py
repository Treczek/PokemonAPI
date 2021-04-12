import mongoengine as me


class Sprite(me.EmbeddedDocument):

    back_default = me.URLField(null=True)
    back_female = me.URLField(null=True)
    back_shiny = me.URLField(null=True)
    back_shiny_female = me.URLField(null=True)
    front_default = me.URLField(null=True)
    front_female = me.URLField(null=True)
    front_shiny = me.URLField(null=True)
    front_shiny_female = me.URLField(null=True)

    @classmethod
    def pick_specified_fields(cls, sprite_dict):
        """
        Filter dictionary fetched from pokemon API using specified Sprite fields.
        """
        return {sprite: sprite_url for sprite, sprite_url in sprite_dict.items() if sprite in cls._fields}


class Encounter(me.EmbeddedDocument):

    note = me.StringField()
    place = me.StringField(required=True)
    timestamp = me.IntField(required=True)


class Pokemon(me.Document):
    base_experience = me.IntField(required=True)
    height = me.IntField(required=True)
    id = me.IntField(me_field='id', primary_key=True)
    name = me.StringField(unique=True, required=True)
    sprites = me.EmbeddedDocumentField(Sprite)
    weight = me.IntField(required=True)
    encounters = me.ListField(me.EmbeddedDocumentField(Encounter))

    meta = {"db_alias": "pokemon_api", 'collection': 'pokemon'}
