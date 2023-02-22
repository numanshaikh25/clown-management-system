from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://clown_user:clown_password@db:5432/clown_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)

class Clown(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User",back_populates='clown')
    contact_name = db.Column(db.String(128))
    contact_email = db.Column(db.String(128))
    contact_number = db.Column(db.String(16))
    
class ClownSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Clown

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    date = db.Column(db.String(128))
    time = db.Column(db.String(128))
    rating = db.Column(db.String(128))
    troupe_leader = db.Column(db.Integer,db.ForeignKey('troupe_leader.id'))
    clown = db.Column(db.Integer,db.ForeignKey('clown.id'))
    client = db.Column(db.Integer,db.ForeignKey('client.id'))
    issues = db.Column(db.String(250),default="")
    status_complete = db.Column(db.Boolean, default=False)

class AppointmentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Appointment