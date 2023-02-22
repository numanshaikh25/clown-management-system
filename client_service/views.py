from flask import Flask, request, jsonify

from models import Client, db, ClientSchema,ma
import requests
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://clown_user:clown_password@db:5432/clown_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
ma.init_app(app)
migrate = Migrate(app, db)


with app.app_context():
    db.create_all()



@app.route('/', methods=['GET'])
def index():
    return jsonify({"info":"Client Service"})


client_schema = ClientSchema()
clients_schema = ClientSchema(many=True)

@app.route("/clients", methods=["GET"])
def get_clients():
    clients = Client.query.all()
    result = clients_schema.dump(clients)
    return jsonify(result.data)

@app.route("/clients", methods=["POST"])
def add_client():
    data = request.json
    client = Client(**data)
    id = client.id
    contact_name = client.contact_name
    contact_number = client.contact_number
    contact_email = client.contact_email
    db.session.add(client)
    db.session.commit()
    return jsonify(contact_name = contact_name, contact_number = contact_number, contact_email = contact_email)

@app.route("/clients/<id>", methods=["GET"])
def get_client(id):
    client = Client.query.get(id)
    return client_schema.jsonify(client)

@app.route("/clients/<id>", methods=["PUT"])
def update_client(id):
    # Check if user is authenticated
    client = Client.query.get(id)
    # if not check_authentication(client.id):
    #     return jsonify({'error': 'Unauthorized'}), 401
    
    
    client.contact_name = request.json['contact_name']
    client.contact_email = request.json['contact_email']
    client.contact_number = request.json['contact_number']
    db.session.commit()
    return client_schema.jsonify(client)

@app.route('/view-appointments/<id>',methods=["GET"])
def view_appointments(id):
    response = requests.get('http://127.0.0.1:5004/view-appointments/'+str(id))
    if response.status_code == 200:
        return response.json(),200
    else:
        
        return response.json(),400

@app.route("/clients/view-appointment/<id>", methods=["GET"])
def view_appointment(id):
    response = requests.get('http://127.0.0.1:5004/view-appointment/'+str(id))
    if response.status_code == 200:
        return response.json(),200
    else:
        
        return response.json(),400

@app.route("/clients/rate-appointment/<id>", methods=["PATCH"])
def rate_appointment(id):
    response = requests.post('http://127.0.0.1:5004/rate-appointment/'+str(id), json=request.json)
    if response.status_code == 200:
        return response.json(),200
    else:
        
        return response.json(),400


if __name__ == '__main__':
    app.run(debug=True)