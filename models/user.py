from models.db import db 

class User(db.Document):
    user_id = db.IntField()
    name = db.StringField(required=True)
    password = db.StringField(required=True)
    email = db.StringField()

