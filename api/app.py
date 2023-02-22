from flask import Flask, request, jsonify
import requests
from flask_jwt_extended import JWTManager, jwt_required, create_access_token,get_jwt_identity
from datetime import timedelta
app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'super-secret'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=10)
jwt = JWTManager(app)

@app.route('/', methods=['GET'])
def index():
    return jsonify({"info":"Backend API"})

#authentication API
@app.route('/api/authentication/register/', methods=["POST"])
def register():
    email = request.json.get('email',None)
    password = request.json.get('password',None)
    role = request.json.get('role',None)
    contact_name = request.json.get("contact_name",None)
    contact_number = request.json.get("contact_number",None)
    contact_email = request.json.get("contact_email",None)
    if not email:
        return jsonify({"error":"Email not present"})
    if not password:
        return jsonify({"error":"Password not present"})
    if not role:
        return jsonify({"error":"Role not present"})
    if not contact_name:
        return jsonify({"error":"Contact name not present"})
    if not contact_number:
        return jsonify({"error":"Contact number not present"})
    if not contact_email:
        return jsonify({"error":"Contact email not present"})

    response = requests.post('http://127.0.0.1:5001/register', json=request.json)
    if response.status_code != 201:
        return response.json(),400

    data = {
        "id" : response.json().get("id"),
        "contact_name" : contact_name,
        "contact_number" : contact_number,
        "contact_email" : contact_email
    }
    if role == "client":
        response = requests.post('http://127.0.0.1:5002/clients', json=data)
        return response.json(), 400
    if role == "troupe_leader":
        response = requests.post('http://127.0.0.1:5003/troupe_leader', json=data)
        return response.json(), 400
    if role == "clown":
        response = requests.post('http://127.0.0.1:5004/clowns', json=data)
        return response.json(), 400

@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email',None)
    password = request.json.get('password',None)
    if not email:
        return jsonify({"error":"Email not present"}),400
    if not password:
        return jsonify({"error":"Password not present"}),400

    response = requests.post('http://127.0.0.1:5001/login', json=request.json)

    if response.status_code == 200:
        user_dict = response.json().get("user")
        access_token = create_access_token(identity=user_dict)
        return jsonify({"message":"Login successful","access_token":access_token,"user":user_dict,}), 200
    else:
        return response.json(), 401

#client API
@app.route("/api/clients/view-appointments/<id>", methods=["GET"])
@jwt_required
def view_client_appointments(id):
    user = get_jwt_identity()
    if user.role!="client":
        return jsonify({"error":"Unauthorized"}),401
    response = requests.get('http://127.0.0.1:5002/clients/view-appointments/'+str(id))
    if response.status_code == 200:
        return response.json(),200
    else:
        
        return response.json(),400

@app.route("/api/clients/view-appointment/<id>", methods=["GET"])
@jwt_required
def view_client_appointment(id):
    user = get_jwt_identity()
    if user.role!="client":
        return jsonify({"error":"Unauthorized"}),401
    response = requests.get('http://127.0.0.1:5002/clients/view-appointment/'+str(id))
    if response.status_code == 200:
        return response.json(),200
    else:
        
        return response.json(),400


@app.route("/api/clients/rate-appointment/<id>", methods=["PATCH"])
@jwt_required
def rate_appointment(id):
    user = get_jwt_identity()
    if user.role!="client":
        return jsonify({"error":"Unauthorized"}),401
    rating = request.json.get("rating",None)
    if not rating:
        return jsonify({"error":"No rating provided"}),400

    response = requests.post('http://127.0.0.1:5002/clients/rate-appointment/'+str(id), json=request.json)
    if response.status_code == 200:
        return response.json(),200
    else:
        
        return response.json(),400



#troupe leader API

@app.route("/api/troup_leader/rate-appointment", methods=["POST"])
@jwt_required
def add_appointment():
    user = get_jwt_identity()
    if user.role!="troupe_leader":
        return jsonify({"error":"Unauthorized"}),401
    data = request.json
    name = request.json.get("name",None)
    date = request.json.get("date",None)
    time = request.json.get("time",None)
    troupe_leader = request.json.get("troupe_leader",None)
    clown = request.json.get("clown",None)
    client = request.json.get("client",None)
    if not name:
        return jsonify({"error":"Name is not provided"})
    if not date:
        return jsonify({"error":"Date is not provided"})
    if not time:
        return jsonify({"error":"Time is not provided"})
    if not troupe_leader:
        return jsonify({"error":"Troupe Leader is not provided"})
    if not clown:
        return jsonify({"error":"Clown is not provided"})
    if not client:
        return jsonify({"error":"Client is not provided"})


    response = requests.post('http://127.0.0.1:5003/troup_leader/add-appointment', json=request.json)
    if response.status_code == 200:
        return response.json(),200
    else:
        
        return response.json(),400
    

#clown API
@app.route("/api/clowns/view-appointments/<id>", methods=["GET"])
@jwt_required
def view_clown_appointments(id):
    user = get_jwt_identity()
    if user.role!="clown":
        return jsonify({"error":"Unauthorized"}),401
    response = requests.get('http://127.0.0.1:5004/clowns/view-appointments/'+str(id))
    if response.status_code == 200:
        return response.json(),200
    else:
        
        return response.json(),400

@app.route("/api/clowns/view-appointment/<id>", methods=["GET"])
@jwt_required
def view_clown_appointment(id):
    user = get_jwt_identity()
    if user.role!="clown":
        return jsonify({"error":"Unauthorized"}),401
    response = requests.get('http://127.0.0.1:5004/clowns/view-appointment/'+str(id))
    if response.status_code == 200:
        return response.json(),200
    else:
        
        return response.json(),400


@app.route("/api/clowns/update-appointment/<id>", methods=["POST"])
@jwt_required
def update_clown_appointment(id):
    user = get_jwt_identity()
    if user.role!="clown":
        return jsonify({"error":"Unauthorized"}),401
    response = requests.post('http://127.0.0.1:5004/clowns/update-appointment/'+str(id),json=request.json)
    if response.status_code == 200:
        return response.json(),200
    else:
        
        return response.json(),400




    
if __name__ == '__main__':
    app.run(debug=True,port=5005)
