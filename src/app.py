"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planets, Favorites, Characters
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def get_all_users():
    users = User.query.all()
    all_users = list(map(lambda x: x.serialize(), users))
    return jsonify(all_users), 200

@app.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    return jsonify(user), 200

@app.route('/user', methods = ['POST'])
def create_user():
    data = request.get_json()
    user = User(email = data['email'], password = data['password'], is_active = True)
    return jsonify(user, 'User has ben successfuly created')
#Characters
@app.route('/characters', methods=['GET'])
def get_all_characters():
    characters = Characters.query.all()
    all_characters = list(map(lambda x: x.serialize(), characters))
    return jsonify(all_characters), 200

@app.route('/characters/<int:id>', methods=['GET'])
def get_characters(id):
    characters = Characters.query.get(id)
    return jsonify(characters), 200

@app.route('/characters', methods = ['POST'])
def create_character():
    data = request.get_json()
    characters = Characters(hair_color = data['hair_color'], eye_color = data['eye_color'], height = data['height'], name = data['name'])
    return jsonify(characters, 'Character has ben successfuly created')

@app.route('/characters/<int:id>', methods=['DELETE'])
def delete_characters(id):
    characters = Characters.query.get(id)
    db.session.delete(characters)
    return jsonify(characters, 'Has Been Deleted'), 200

#Planets 
@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets = Planets.query.all()
    all_planets = list(map(lambda x: x.serialize(), planets))
    return jsonify(all_planets), 200

@app.route('/planets/<int:id>', methods=['GET'])
def get_planets(id):
    planets = Planets.query.get(id)
    return jsonify(planets), 200

@app.route('/planets', methods = ['POST'])
def create_planets():
    data = request.get_json()
    planets = Planets(diameter = data['diameter'], rotational_period = data['rotational_period'], climate = data['climate'], population = data['population'])
    return jsonify(planets, 'Planet has ben successfuly created')

@app.route('/planets/<int:id>', methods=['DELETE'])
def delete_planets(id):
    planets = Planets.query.get(id)
    db.session.delete(planets)
    return jsonify(planets, 'Has Been Deleted'), 200

# #Favorites
@app.route('/favorites', methods=['GET'])
def get_all_favorites():
    favorites = Favorites.query.all()
    all_favorites = list(map(lambda x: x.serialize(), favorites))
    return jsonify(all_favorites), 200

@app.route('/favorites/<int:id>', methods=['GET'])
def get_favorites(id):
    favorites = Favorites.query.get(id)
    return jsonify(favorites), 200

@app.route('/favorites', methods = ['POST'])
def create_favorites():
    data = request.get_json()
    favorites = favorites(character = data['characters'], user = data['user'], planets = data['planets'])
    return jsonify(favorites, 'favorites has ben successfuly created')

@app.route('/favorites/<int:id>', methods=['DELETE'])
def delete_favorites(id):
    favorites = Favorites.query.get(id)
    db.session.delete(favorites)
    return jsonify(favorites, 'Has Been Deleted'), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

