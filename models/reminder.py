from mongoengine import *
from models.db import db 
from models.event import Event

class Reminder(db.Document):
    event = db.ReferenceField(Event, required=True, reverse_delete_rule=CASCADE)
    time = db.DateTimeField(required=True)
