#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from email.policy import default
import json
import os
from unicodedata import name
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
import config

# Models
from models import Genre, db, Venue, Artist, Show, Location

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)
migrate = Migrate(app,db)

# connect to a local postgresql database
app.config["SQLALCHEMY_DATABASE_URI"]=(config.SQLALCHEMY_DATABASE_URI)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  data = []
  venue_list = []
  locations = Location.query.all()
  
  for location in locations:
    venues = Venue.query.filter_by(location_id=location.id)
    for venue in venues:
      venue_list.append({
        "id": venue.id,
        "name": venue.name,
        "num_upcoming_shows": len(venue.shows),
      })
    loc = {
      "city": location.city,
      "state": location.state,
      "venues": venue_list
    }
    venue_list = []
    data.append(loc)
  # print(f"json {json.dumps(data)}")

  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  venues=[]
  search = f"%{request.form.get('search_term', '')}%"
  venues_query = Venue.query.filter(Venue.name.ilike(search)).all()
  
  for venue in venues_query:
    comming_shows_query = db.session.query(Show).join(Venue).filter(Show.venue_id==venue.id).filter(Show.start_time>=datetime.now()).all()
    venues.append({
        "id": venue.id,
        "name": venue.name,
        "num_upcoming_shows": len(comming_shows_query),
    })
  response={
    "count": len(venues),
    "data": venues
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # replace with real venue data from the venues table, using venue_id
  venue = Venue.query.filter_by(id=venue_id).first()
  past_shows_query = db.session.query(Show).join(Venue).filter(Show.venue_id==venue_id).filter(Show.start_time<datetime.now()).all()
  comming_shows_query = db.session.query(Show).join(Venue).filter(Show.venue_id==venue_id).filter(Show.start_time>=datetime.now()).all()
  past_shows = []
  comming_shows = []
  genres = []
  for show in past_shows_query:
    past_shows.append(
      {
        "artist_id": show.artist_id,
        "artist_name": show.artist.name,
        "artist_image_link": show.artist.website_link,
        "start_time": format_datetime(show.start_time.strftime('%m/%d/%Y'), "full")
      }
    )
  for show in comming_shows_query:
    comming_shows.append(
      {
        "artist_id": show.artist_id,
        "artist_name": show.artist.name,
        "artist_image_link": show.artist.website_link,
        "start_time": format_datetime(show.start_time.strftime('%m/%d/%Y'), "full")
      }
    )

  for genre in venue.genres:
    genres.append(genre.name)
  
  data = {
    "id": venue.id,
    "name": venue.name,
    "genres": genres,
    "address": venue.address,
    "city": venue.location.city,
    "state": venue.location.state,
    "phone": venue.phone,
    "website": venue.website_link,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "image_link": venue.image_link,
    "past_shows": past_shows,
    "upcoming_shows": comming_shows ,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(comming_shows),
  }
  
  return render_template('pages/show_venue.html', venue=data)

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # insert form data as a new Venue record in the db, instead
  # modify data to be the data object returned from db insertion
  form = VenueForm()
  error = False
  genres = []
  try:
    location = Location.query.filter(Location.city==form.city.data).first()
    if location == None:
      location = Location(city=form.city.data, state=form.state.data)
    for genre in form.genres.data:
      genre_query = Genre.query.filter_by(name=genre).first()
      if genre_query != None:
        genres.append(genre_query)
      else:
        genres.append(Genre(name=genre))

    venue = Venue(
      genres=genres,
      name=form.name.data,
      location=location,
      address=form.address.data,
      phone=form.phone.data,
      image_link=form.image_link.data,
      facebook_link=form.facebook_link.data,
      website_link=form.website_link.data,
      seeking_talent=form.seeking_talent.data,
      seeking_description=form.seeking_description.data
    )

    db.session.add(venue)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
  finally:
    db.session.close()
  if error == True:
  # on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    flash('Error creating venue' + form.name.data + ' try again.')
    return render_template('forms/new_venue.html', form=form)

  # on successful db insert, flash success
  flash('Venue ' + request.form['name'] + ' was successfully listed!')
  return render_template('pages/home.html')

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()

  # populate form with values from venue with ID <venue_id>
  venue = Venue.query.filter_by(id=venue_id).first()
  form.name.data = venue.name
  form.city.data = venue.location.city
  form.state.data = venue.location.state
  form.address.data = venue.address
  form.phone.data = venue.phone
  form.image_link.data = venue.image_link
  form.facebook_link.data = venue.facebook_link
  form.website_link.data = venue.website_link
  form.seeking_talent.data = venue.seeking_talent
  form.seeking_description.data = venue.seeking_description

  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  form = VenueForm()
  error = False
  genres=[]
  venue = Venue.query.get(venue_id)

  try:
    location = Location.query.filter(Location.city==form.city.data).first()
    if location == None:
      location = Location(city=form.city.data, state=form.state.data)
    
    for genre in form.genres.data:
      genre_query = Genre.query.filter_by(name=genre).first()
      if genre_query != None:
        genres.append(genre_query)
      else:
        genres.append(Genre(name=genre))
    print("here")
    venue.name=form.name.data
    venue.genres=genres
    venue.location=location
    venue.address=form.address.data
    venue.phone=form.phone.data
    venue.image_link=form.image_link.data
    venue.facebook_link=form.facebook_link.data
    venue.website_link=form.website_link.data
    venue.seeking_talent=form.seeking_talent.data
    venue.seeking_description=form.seeking_description.data
    print(venue)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
  finally:
    db.session.close()
  if error == True:
    flash('Error editing venue' + form.name.data + ' try again.')
    return render_template('forms/edit_venue.html', form=form, venue=venue)

  flash('Venue ' + request.form['name'] + ' was successfully edited!')
  return redirect(url_for('show_venue', venue_id=venue_id))

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  try:
      Venue.query.filter_by(id=venue_id).delete()
      db.session.commit()
  except:
      db.session.rollback()
  finally:
      db.session.close()
  return render_template('pages/home.html')

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # replace with real data returned from querying the database
  data = Artist.query.all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search = f"%{request.form.get('search_term','')}%"
  artists_query = Artist.query.filter(Artist.name.ilike(search)).all()
  artists=[]
  for artist in artists_query:
    comming_shows = db.session.query(Show).join(Artist).filter(Show.artist_id==artist.id).filter(Show.start_time>=datetime.now()).all()
    artists.append({
      "id": artist.id,
      "name": artist.name,
      "num_upcoming_shows": len(comming_shows),
    })
  response={
    "count": len(artists),
    "data": artists
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # replace with real artist data from the artist table, using artist_id
  artist = Artist.query.filter_by(id=artist_id).first()
  past_shows_query = db.session.query(Show).join(Artist).filter(Show.artist_id==artist_id).filter(Show.start_time<datetime.now()).all()
  comming_shows_query = db.session.query(Show).join(Artist).filter(Show.artist_id==artist_id).filter(Show.start_time>=datetime.now()).all()
  past_shows = []
  comming_shows = []
  genres = []
  for show in past_shows_query:
    past_shows.append(
      {
      "venue_id": show.venue.id,
      "venue_name":show.venue.name,
      "venue_image_link": show.venue.image_link,
      "start_time": format_datetime(show.start_time.strftime('%m/%d/%Y'), "full")
      }
    )
  for show in comming_shows_query:
    comming_shows.append(
      {
      "venue_id": show.venue.id,
      "venue_name":show.venue.name,
      "venue_image_link": show.venue.image_link,
      "start_time": format_datetime(show.start_time.strftime('%m/%d/%Y'), "full")
      }
    )
  for genre in artist.genres:
    genres.append(genre.name)

  data = {
    "id": artist.id,
    "name": artist.name,
    "genres": genres,
    "city": artist.location.city,
    "state": artist.location.state,
    "phone": artist.phone,
    "seeking_venue": artist.seeking_venue,
    "facebook_link": artist.facebook_link,
    "website": artist.website_link,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link,
    "past_shows": past_shows,
    "upcoming_shows": comming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(comming_shows),
  }
  return render_template('pages/show_artist.html', artist=data)

@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  
  # populate form with fields from artist with ID <artist_id>
  artist=Artist.query.get(artist_id)

  form.name.data = artist.name
  form.phone.data = artist.phone
  form.image_link.data = artist.image_link
  form.facebook_link.data = artist.facebook_link
  form.website_link.data = artist.website_link
  form.seeking_venue.data = artist.seeking_venue
  form.seeking_description.data = artist.seeking_description
  form.city.data = artist.location.city
  form.state.data = artist.location.state

  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  form = ArtistForm()
  error = False
  genres=[]
  artist = Artist.query.get(artist_id)

  try:
    location = Location.query.filter(Location.city==form.city.data).first()
    if location == None:
      location = Location(city=form.city.data, state=form.state.data)
    
    for genre in form.genres.data:
      genre_query = Genre.query.filter_by(name=genre).first()
      if genre_query != None:
        genres.append(genre_query)
      else:
        genres.append(Genre(name=genre))

    artist.name=form.name.data
    artist.phone=form.phone.data
    artist.image_link=form.image_link.data
    artist.facebook_link=form.facebook_link.data
    artist.website_link=form.website_link.data
    artist.seeking_venue=form.seeking_venue.data
    artist.seeking_description=form.seeking_description.data
    artist.location=location
    artist.genres=genres

    db.session.commit()
  except:
    error = True
    db.session.rollback()
  finally:
    db.session.close()
  if error == True:
    flash('Error editing artist' + form.name.data + ' try again.')
    return render_template('forms/edit_artist.html', form=form, artist=artist)

  flash('Artist ' + request.form['name'] + ' was successfully edited!')
  
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # insert form data as a new Artist record in the db, instead
  # modify data to be the data object returned from db insertion
  form = ArtistForm()
  error = False
  genres = []
  try:
    location = Location.query.filter(Location.city==form.city.data).first()
    if location == None:
      location = Location(city=form.city.data, state=form.state.data)
    for genre in form.genres.data:
      genre_query = Genre.query.filter_by(name=genre).first()
      if genre_query != None:
        genres.append(genre_query)
      else:
        genres.append(Genre(name=genre))

    artist = Artist(
      name=form.name.data,
      phone=form.phone.data,
      image_link=form.image_link.data,
      facebook_link=form.facebook_link.data,
      website_link=form.website_link.data,
      seeking_venue=form.seeking_venue.data,
      seeking_description=form.seeking_description.data,
      location=location,
      genres=genres
    )

    db.session.add(artist)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
  finally:
    db.session.close()
  if error == True:
    flash('Error creating Artist' + form.name.data + ' try again.')
    return render_template('forms/new_artist.html', form=form)

  flash('Artist ' + request.form['name'] + ' was successfully listed!')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # replace with real venues data.
  show_query = Show.query.all()
  data = []
  for show in show_query:
    data.append(
      {
        "venue_id": show.venue_id,
        "venue_name": show.venue.name,
        "artist_id": show.artist_id,
        "artist_name": show.artist.name,
        "artist_image_link": show.artist.image_link,
        "start_time": format_datetime(show.start_time.strftime('%m/%d/%Y'), "full")
      }
    )

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # insert form data as a new Show record in the db, instead

  form = ShowForm()
  error = False
  genres = []
  try:
    show = Show(
      artist_id=form.artist_id.data,
      venue_id=form.venue_id.data,
      start_time=form.start_time.data
    )

    db.session.add(show)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
  finally:
    db.session.close()
  if error == True:
    flash('Error creating Show try again.')
    return render_template('forms/new_show.html', form=form)

  flash('Show was successfully listed!')
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.debug=config.DEBUG
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port)

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
