#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    # city = db.Column(db.String(120))
    # state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(120))

    # One-to-Many Show
    # shows = db.relationship('Show', backref='venue', collection_class = list, lazy=True)
    shows = db.relationship('Show', backref='venue', lazy=False)

    # Many-to-One Location
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)

    # TODO: implement any missing fields, as a database migration using Flask-Migrate


class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    # city = db.Column(db.String(120))
    # state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(120))

    shows = db.relationship('Show', backref='show', lazy=True)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False, default=1)

    def __repr__(self):
      return '<Artist %r>' % self.name

    # One-to-One Show
    # One-to-One Location

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Location(db.Model):
  __tablename__ = 'locations'

  id = db.Column(db.Integer, primary_key=True)
  city = db.Column(db.String(120))
  state = db.Column(db.String(120))

  venues = db.relationship('Venue', backref='location', lazy=False)
  artists = db.relationship('Artist', backref='location', lazy=False)

  def __repr__(self):
      return '<Location %r>' % self.city

# class Genre(db.Model):
#   __tablename__ = "genres"


# class Contact(db.Model):
#   __tablename__ = 'contacts'

#   id = db.Column(db.Integer, primary_key=True)
#   phone = db.Column(db.String(120))
#   genres = db.Column(db.String(120))
#   image_link = db.Column(db.String(500))
#   facebook_link = db.Column(db.String(120))
#   website_link = db.Column(db.String(120))

#   def __repr__(self):
#       return '<Contact %r>' % self.phone

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Show(db.Model):
  __tablename__ = 'shows'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(120))
  
  venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'), nullable=False)

  artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable=False)
  artist = db.relationship('Artist', backref=db.backref('show', lazy=True))
  
  start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

  def __repr__(self):
        return '<Show %r>' % self.name

  # One-to-One Venue
  # One-to-One Artist
