from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Planets(db.Model):
    __tablename__ = 'planets'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    diameter = db.Column(db.String(250), nullable=False)
    rotational_period = db.Column(db.String(250), nullable=False)
    climate = db.Column(db.String(250), nullable=False)
    population = db.Column(db.String(250), nullable=False)
    

    def serialize(self):
        return {
            "diameter": self.diameter,
            "rotational_period": self.rotational_period,
            "climate": self.climate,
            "population": self.population,
        }
    
class Characters(db.Model):
    __tablename__ = 'characters'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    hair_color = db.Column(db.String(250), nullable=False)
    eye_color = db.Column(db.String(250), nullable=False)
    height = db.Column(db.String(250), nullable=False)
    name = db.Column(db.String(250), nullable=False)
    

    def serialize(self):
        return {
            "hair_color": self.hair_color,
            "eye_color": self.eye_color,
            "height": self.height,
            "name": self.name,
        }
    
class Favorites(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    character_id = db.Column(db.Integer, db.ForeignKey("characters.id"), nullable=True)
    planet_id = db.Column(db.Integer, db.ForeignKey("planets.id"), nullable=True)
    
    user=db.relationship(User)
    characters=db.relationship(Characters)
    planets=db.relationship(Planets)

    def serialize(self):
        return {
            "user_id": self.user_id,
            "character_id": self.character_id,
            "planet_id": self.planet_id,
        }

