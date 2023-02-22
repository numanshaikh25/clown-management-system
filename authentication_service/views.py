from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from models import User, db,ma
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://clown_user:clown_password@db:5432/clown_db'
app.config['SQLALCHEMY_BINDS'] = {'clown_db': 'postgresql://clown_user:clown_password@db:5432/clown_db'}
db.init_app(app)
ma.init_app(app)
migrate = Migrate(app, db)
# user_schema = UserSchema()


@app.route('/', methods=['GET'])
def index():
    return jsonify({"info":"Authentication Service"})

@app.route('/register', methods=['POST'])
def register():
    email = request.json.get('email')
    password = request.json.get('password')
    role = request.json.get('role')
    # check_user = User.query.filter_by(email=email)  
    # if check_user:
    #     return jsonify({'message' : 'User with this email already exists'}),400
    user = User(email=email, password=password,role=role)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        user_dict ={"id":user.id,"email":user.email,"role":user.role}
        # user_dict = user_schema.dump(user)
        # user_dict.pop('password')
        return jsonify({'message': 'Login successful','user':user_dict}), 200
    else:
        return jsonify({'message': 'Wrong email or password'}), 401

with app.app_context():
    db.create_all()

    
if __name__ == '__main__':
    app.run(debug=True)
