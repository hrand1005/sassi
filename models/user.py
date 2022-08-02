from models.db import db 

class User(db.Document):
    user_id = db.IntField()
    name = db.StringField()
    # hashed, obviously :)
    password = db.StringField()
    email = db.StringField()

    def to_json(self):
        return {"id": self.user_id,
                "name": self.name,
                "email": self.email}
