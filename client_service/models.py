from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


db = SQLAlchemy()
ma = Marshmallow()

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", back_populates="client")
    contact_name = db.Column(db.String(128))
    contact_email = db.Column(db.String(128))
    contact_number = db.Column(db.String(16))
    def __init__(self,user_id,contact_name,contact_email,contact_number):
        self.user_id = user_id
        self.contact_name = contact_name
        self.contact_email = contact_email
        self.contact_number = contact_number

class ClientSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Client
