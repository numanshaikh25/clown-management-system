from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import Troupe_Leader, Troupe_LeaderSchema, db,ma
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://clown_user:clown_password@db:5432/clown_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
ma.init_app(app)
migrate = Migrate(app, db)


@app.route('/', methods=['GET'])
def index():
    return jsonify({"info":"Troupe Leader Service"})

troupe_leader_schema = Troupe_LeaderSchema()
troupe_leaders_schema = Troupe_LeaderSchema(many=True)

@app.route("/troupe_leaders", methods=["GET"])
def get_troupe_leaders():
    troupe_leaders = Troupe_Leader.query.all()
    result = troupe_leader_schema.dump(troupe_leaders)
    return jsonify(result.data)

@app.route("/troupe_leader", methods=["POST"])
def add_troupe_leader():
    # Check if user is authenticated
    id = request.json.get('id')
    data = request.json
    data.pop('id')
    troupe_leader = Troupe_Leader(user_id=id, **data)
    # if not check_authentication(client.id):
    #     return jsonify({'error': 'Unauthorized'}), 401

    db.session.add(troupe_leader)
    db.session.commit()
    return troupe_leaders_schema.jsonify(troupe_leader)

@app.route("/troupe_leader/<id>", methods=["GET"])
def get_troupe_leader(id):
    troupe_leader = Troupe_Leader.query.get(id)
    return troupe_leaders_schema.jsonify(troupe_leader)

@app.route("/troupe_leader/<id>", methods=["PUT"])
def update_troupe_leader(id):
    # Check if user is authenticated
    troupe_leader = Troupe_Leader.query.get(id)
    # if not check_authentication(client.id):
    #     return jsonify({'error': 'Unauthorized'}), 401
    
    
    troupe_leader.contact_name = request.json['contact_name']
    troupe_leader.contact_email = request.json['contact_email']
    troupe_leader.contact_number = request.json['contact_number']
    db.session.commit()
    return troupe_leader_schema.jsonify(troupe_leader)
 

@app.route('/troupe_leader/add-appointment',methods=["POST"])
def add_appointment():

    response = requests.post('http://127.0.0.1:5004/add-appointment/', json=request.json)
    if response.status_code == 201:
        return response.json(),201
    else:
        
        return response.json(),400

    
if __name__ == '__main__':
    app.run(debug=True)
