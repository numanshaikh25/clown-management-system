from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import Appointment,AppointmentSchema,Clown, ClownSchema, db,ma


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://clown_user:clown_password@db:5432/clown_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
ma.init_app(app)
migrate = Migrate(app, db)


@app.route('/', methods=['GET'])
def index():
    return jsonify({"info":"Clown Service"})

clown_schema = ClownSchema()
clowns_schema = ClownSchema(many=True)
appointment_schema = AppointmentSchema()
appointments_schema = AppointmentSchema(many=True)

@app.route("/clowns", methods=["GET"])
def get_clowns():
    clowns = Clown.query.all()
    result = clowns_schema.dump(clowns)
    return jsonify(result.data)

@app.route("/clowns", methods=["POST"])
def add_clown():
    # Check if user is authenticated
    id = request.json.get('id')
    data = request.json
    data.pop('id')
    clown = Clown(user_id=id, **data)
    # if not check_authentication(client.id):
    #     return jsonify({'error': 'Unauthorized'}), 401

    db.session.add(clown)
    db.session.commit()
    return clown_schema.jsonify(clown)

@app.route("/clowns/<id>", methods=["GET"])
def get_clown(id):
    clown = Clown.query.get(id)
    return clown_schema.jsonify(clown)

@app.route("/clowns/<id>", methods=["PUT"])
def update_clown(id):
    # Check if user is authenticated
    clown = Clown.query.get(id)
    # if not check_authentication(client.id):
    #     return jsonify({'error': 'Unauthorized'}), 401
    
    
    clown.contact_name = request.json['contact_name']
    clown.contact_email = request.json['contact_email']
    clown.contact_number = request.json['contact_number']
    db.session.commit()
    return clown_schema.jsonify(clown)

@app.route("/clowns/appointments/<id>",methods=["GET"])
def view_appointments_clown(id):
    if Appointment.query.filter_by(clown=id).exists():
        appointments = Appointment.query.filter_by(id)
        result = appointments_schema.dump(appointments)
        return jsonify(result.data),200
    else:
        return jsonify({"error":"Appointment does not exist"})

@app.route('/clowns/view-appointment/<id>',methods=["GET"])
def view_appointment_clown(id):
    if Appointment.query.filter_by(id=id).exists():
        appointment = Appointment.query.get(id)
        return appointment_schema.jsonify(appointment),200
    else:
        return jsonify({"error":"Appointment does not exist"})


@app.route("/clowns/appointment-issue/<id>",methods=["PATCH"])
def report_appointment_issue(id):
    if Appointment.query.filter_by(id=id).exists():
        appointment = Appointment.query.get(id)
        appointment.issues = request.json.get("issues")
        db.session.commit()
        return appointment_schema.jsonify(appointment),200
    else:
        return jsonify({"error":"Appointment does not exist"})


@app.route('/view-appointments/<id>',methods=["GET"])
def view_client_appointments(id):
    if Appointment.query.filter_by(client=id).exists():
        appointments = Appointment.query.filter_by(id)
        result = appointments_schema.dump(appointments)
        return jsonify(result.data),200
    else:
        return jsonify({"error":"Appointment does not exist"})

@app.route('/view-appointment/<id>',methods=["GET"])
def view_client_appointment(id):
    if Appointment.query.filter_by(id=id).exists():
        appointment = Appointment.query.get(id)
        return appointment_schema.jsonify(appointment),200
    else:
        return jsonify({"error":"Appointment does not exist"})

@app.route('/rate-appointment/<id>',methods=["POST"])
def update_appointment(id):
    if Appointment.query.filter_by(id=id).exists():
        appointment = Appointment.query.get(id)
        if appointment.status_complete==False:
            name = request.json.get("name",None)
            date = request.json.get("date",None)
            time = request.json.get("time",None)
            if name:
                appointment.name = name
            if date:
                appointment.date = date
            if time:
                appointment.time = time
            db.session.commit()
            return appointment_schema.jsonify(appointment),200
        else:
            return jsonify({"error":"Appointment has been not completed yet"})
    else:
        return jsonify({"error":"Appointment does not exist"})

@app.route('/update-appointment/<id>',methods=["POST"])
def rate_appointment(id):
    if Appointment.query.filter_by(id=id).exists():
        appointment = Appointment.query.get(id)
        if appointment.status_complete:
            appointment.rating = request.json.get("rating")
            db.session.commit()
            return appointment_schema.jsonify(appointment),200
        else:
            return jsonify({"error":"Appointment has been not completed yet"})
    else:
        return jsonify({"error":"Appointment does not exist"})


#external services
@app.route('/add-appointment',methods=["POST"])
def add_appointment():
    data = request.json
    date = request.json.get("date")
    time = request.json.get("time")
    clown = request.json.get("clown")
    if Appointment.query.filter_by(clown=clown,date=date,time=time).exists():
        return jsonify({"error":"Appointment already booked for that schedule"})
    appointment = Appointment(**data)
    db.session.add(appointment)
    db.session.commit()

    return appointment_schema.jsonify(appointment),201

  
if __name__ == '__main__':
    app.run(debug=True)

