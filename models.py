#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

genre_artist = db.Table('genre_artist',
    db.Column('genre_id', db.Integer, db.ForeignKey('genres.id')),
    db.Column('artis_id', db.Integer, db.ForeignKey('artists.id'))
)

genre_venue = db.Table('genre_venue',
    db.Column('genre_id', db.Integer, db.ForeignKey('genres.id')),
    db.Column('venue_id', db.Integer, db.ForeignKey('venues.id'))
)

# implement any missing fields, as a database migration using Flask-Migrate
class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    # city = db.Column(db.String(120))
    # state = db.Column(db.String(120))
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    # genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(120))

    # One-to-Many Show
    # shows = db.relationship('Show', backref='venue', collection_class = list, lazy=True)
    shows = db.relationship('Show', backref='venue', lazy=False)
    genres = db.relationship('Genre',secondary=genre_venue, backref='venues', lazy=True)

    # Many-to-One Location
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)

    def __repr__(self) -> str:
        return f"Venue: \
            {self.name} \
            {self.location_id} \
            {self.address} \
            {self.phone} \
            {self.image_link} \
            {self.facebook_link} \
            {self.website_link} \
            {self.seeking_talent} \
            {self.seeking_description} \
            {self.genres } \
            "


class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    # city = db.Column(db.String(120))
    # state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    # genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(120))

    shows = db.relationship('Show', backref='artist', lazy=True)
    genres = db.relationship('Genre',secondary=genre_artist, backref='artists', lazy=True)

    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)

    def __repr__(self):
      return '<Artist %r>' % self.name

    # One-to-One Show
    # One-to-One Location

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Location(db.Model):
  __tablename__ = 'locations'

  id = db.Column(db.Integer, primary_key=True)
  city = db.Column(db.String(120), nullable=False)
  state = db.Column(db.String(120), nullable=False)

  venues = db.relationship('Venue', backref='location', lazy=False)
  artists = db.relationship('Artist', backref='location', lazy=False)

  def __repr__(self):
      return '<Location %r>' % self.city

class Genre(db.Model):
    __tablename__ = "genres"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)

    def __repr__(self) -> str:
        return f'<Genre> {self.name}'


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
  
  venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'), nullable=False)

  artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable=False)
  
  start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

  def __repr__(self):
        return f"<Show \
            {self.venue_id} \
            {self.artist_id} \
            >"

  # One-to-One Venue
  # One-to-One Artist
