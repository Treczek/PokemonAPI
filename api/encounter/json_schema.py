from flask_restx import fields

encounter_post = {
    'place': fields.String(required=True),
    'note': fields.String()
}

encounter_get = {
    'place': fields.String(required=True),
    'note': fields.String(),
    'timestamp': fields.Integer(required=True)
}
