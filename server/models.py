from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, ForeignKey
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)


class Planet(db.Model, SerializerMixin):
    __tablename__ = 'planets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    distance_from_earth = db.Column(db.Integer)
    nearest_star = db.Column(db.String)
    mission_id = db.Column(db.Integer, db.ForeignKey('missions.id'))
    
    # Add relationship planet can have many missions
    mission = db.relationship('Mission', backref=db.backref('planet', uselist=False))

    #add relationship planet can have many scientists through missions
    scientists = db.relationship('Scientist', secondary='missions')


    # Add serialization rules
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'distance_from_earth': self.distance_from_earth,
            'nearest_star': self.nearest_star
        }


class Scientist(db.Model, SerializerMixin):
    __tablename__ = 'scientists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    field_of_study = db.Column(db.String)
    planet_id = db.column(db.Integer, db.ForeignKey('planets.id'))


    # Add relationship to planets
    planet = db.relationship('Planet', backref='scientists')
    #relationship of missions through missions
    missions = db.relationship('Mission', secondary='missions')

    # Add serialization rules
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'field_of_study': self.field_of_study,
            'planet_id': self.planet_id
        }

    # Add validation


class Mission(db.Model, SerializerMixin):
    __tablename__ = 'missions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id', ondelete='CASCADE'))
    scientist_id = db.Column(db.Integer, db.ForeignKey('scientists.id', ondelete='CASCADE'))

     # Add relationships
                             
    planet = db.relationship('Planet', backref='missions')
    scientists = db.relationship('Scientist', backref='missions')

   
    # Add serialization rules
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'planet_id': self.planet_id,
            'scientists_id': self.scientist_id
    }

    # Add validation


# add any models you may need.
