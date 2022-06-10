#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from ast import dump
from email.policy import default
import json
from types import CoroutineType
from typing import final
from unicodedata import name
from unittest.case import _AssertRaisesContext
import dateutil.parser
import datetime
import babel
from flask import Flask, render_template, request, Response, flash, redirect, session, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import FlaskForm
from forms import *
from os import abort
import sys
from forms import VenueForm
from models import Venue, Show, Artist, db, app
from utils import get_upcoming_shows, get_past_shows

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
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  areas = []
  error= {}
  try:
      results = Venue.query.distinct(Venue.city, Venue.state).all()
      for result in results:
        resultDict = { "city": result.city, "state": result.state,
        }
        venues = Venue.query.filter_by(city = result.city, state = result.state).all()

        venues_temp  = {}
        venues_formatted = []
        for venue in venues:
          upcoming_shows = get_upcoming_shows(venue.shows)
          venues_temp["id"], venues_temp["name"], venues_temp["num_upcoming_shows"]  = venue.id, venue.name, len(upcoming_shows)
          venues_formatted.append(venues_temp)
        resultDict["venues"] = venues_formatted
        areas.append(resultDict)
  except:
    db.session.rollback()
    error = True
  finally:
    db.session.close()
    if error: 
      flash('Could not fetch venues')
    return render_template('pages/venues.html', areas=areas)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on venues with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term = request.form.get('search_term', '')
  results = Venue.query.filter(
  Venue.name.ilike(f'%{search_term}%') |
  Venue.city.ilike(f'%{search_term}%') |
  Venue.state.ilike(f'%{search_term}%')
  ).all()

  response={
    "count": len(results),
    "data": []
  }

  for result in results:
    result_data = {
      "id": result.id,
      "name": result.name
    }

    upcoming_shows = 0 
    for show in result.shows:
      if show.start_time >  datetime.now():
        upcoming_shows += 1
        print(show)
    result_data['id'], result_data['name'], result_data["num_upcoming_show"] = result.id, result.name, upcoming_shows
    response["data"].append(result_data)
  return render_template('pages/search_venues.html', results=response, search_term=search_term)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  venue = Venue.query.get(venue_id)
  setattr(venue, "genres", venue.genres.split(","))
  setattr(venue, "seeking_description", venue.seeking_desc)

  all_past_shows = get_past_shows(venue.shows)
  all_upcoming_shows =  get_upcoming_shows(venue.shows)

  temp_past_shows = []
  temp_upcoming_shows = []

  for show in all_past_shows:
      past_show = {
        "venue_id": show.venues.id,
        "venue_name": show.venues.name,
        "image_link": show.venues.image_link,
        "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M:%S")
      }
      temp_past_shows.append(past_show)
      setattr(venue, "past_shows", temp_past_shows)

  for show in all_upcoming_shows:
    current_upcoming_show = {
      "venue_id":show.venue.id,
      "venue_name": show.venue.venue_name,
      "venue_image_link": show.venue.image_link,
      "start_time": show.venue["start_time"].strftime("%m/%d/%Y, %H:%M:%S")
    }
    temp_upcoming_shows.append(current_upcoming_show)
    setattr(venue, "upcoming_show", temp_upcoming_shows)

    #append number of upcoming_shows and past_shows to artist object
    setattr(venue, "past_shows_count", len(temp_past_shows))
    setattr(venue, "upcoming_shows_count", len(temp_upcoming_shows))
  return render_template('pages/show_venue.html', venue=venue)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  error = False
  data = {}
  form = VenueForm(request.form)
  try:  
    if request.method == "POST":
        name = form.name.data
        city = form.city.data
        state = form.state.data
        phone =  form.phone.data
        address = form.address.data
        genres = ",".join(form.genres.data)
        image_link = form.image_link.data
        facebook_link = form.facebook_link.data
        website_link = form.website_link.data
        seeking_talent= form.seeking_talent.data
        seeking_desc = form.seeking_description.data
        new_venue = Venue(name=name,city=city,state=state,phone=phone,
        genres=genres,image_link=image_link,
        facebook_link=facebook_link,website_link=website_link,
        seeking_talent=seeking_talent, address=address, seeking_desc=seeking_desc)
        db.session.add(new_venue)
        db.session.commit()
        flash('Venue ' + form.name.data + ' was successfully listed!')
        # data = new_venue
      # print(data)
      # TODO: modify data to be the data object returned from db insertion
      # on successful db insert, flash success
  except:
      db.session.rollback()
      error = True
  finally:
          db.session.close()
  if error:
    flash('An error occurred. Venue ' + form.name.data + ' could not be listed.')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html', data=data)

        

  # on successful db insert, flash success
  # TODO: on unsuccessful db insert, flash an error instead.
  # flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html', data=data)

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None                                                     

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  error = False
  # Make some changes here
  try: 
    artists = db.session.query(Artist.id, Artist.name).all()
  except:
    db.session.rollback()
    error = True
  finally:
    db.session.close()
  if error:
    flash('Could not fetch artists')
  return render_template('pages/artists.html', artists=artists)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term = request.form.get('search_term', '')
 
  results = Artist.query.filter(
    Artist.name.ilike(f'%{search_term}%') |
    Artist.city.ilike(f'%{search_term}%') |
    Artist.state.ilike(f'%{search_term}%')
    ).all()

  response = {
    "count": len(results),
    "data":[]
  }

  for result in results:
    result_data = {}
    result_data["id"], result_data["name"] =  result.id, result.name
    upcoming_shows = 0
    for show in result.shows:
      if show.start_time > datetime.datetime.now():
        upcoming_shows = upcoming_shows + 1
    result_data["num_upcoming_show"] = upcoming_shows
    response["data"].append(result_data)

  return render_template('pages/search_artists.html', results=response, search_term=search_term)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
    artist = Artist.query.get(artist_id)
    setattr(artist, "genres", artist.genres.split(",")) # convert genre string back to array

    all_past_shows = get_past_shows(artist.shows)
    all_upcoming_shows =  get_upcoming_shows(artist.shows)
    
    temp_past_shows = []
    temp_upcoming_shows = []

    for show in all_past_shows:
      past_show = {
        "venue_id": show.venues.id,
        "venue_name":   show.venues.name,
        "venue_image_link": show.venues.image_link,
        "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M:%S")
      }

      temp_past_shows.append(past_show)
      setattr(artist, "past_shows", temp_past_shows)

    for show in all_upcoming_shows:
      current_upcoming_show = {
        "venue_id":show.venue.id,
        "venue_name": show.venue.name,
        "venue_image_link": show.venue.image_link,
        "start_time": show.venue["start_time"].strftime("%m/%d/%Y, %H:%M:%S")
      }
      temp_upcoming_shows.append(current_upcoming_show)
      setattr(artist, "upcoming_show", temp_upcoming_shows)

      #append number of upcoming_shows and past_shows to artist object
      setattr(artist, "past_shows_count", len(temp_past_shows))
      setattr(artist, "upcoming_shows_count", len(temp_upcoming_shows))

    return render_template('pages/show_artist.html', artist=artist)
        

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.get(artist_id)
  form.genres.data = artist.genres.split(",") # convert genre string back to array

  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  form = ArtistForm(request.form)
  if request.method == 'POST':
      try:
        artist = Artist.query.get(artist_id)

        artist.name = form.name.data
        artist.city = form.city.data
        artist.state = form.state.data
        artist.phone = form.phone.data
        #convert the genres to string in order to save it into the db
        artist.genres=",".join(form.genres.data)
        artist.image_link = form.image_link.data
        artist.facebook_link = form.facebook_link.data
        artist.website_link =  form.website_link.data
        artist.seeking_venues = form.seeking_venue.data
        artist.seeking_desc =  form.seeking_description.data

        db.session.add(artist)
        db.session.commit()

        flash("Record for " + artist.name + "has been updated!")
      except:
        db.session.rollback()
        print(sys.exc_info)
      finally:
        db.session.close()

        
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.get(venue_id)
  form.genres.data = venue.genres.split(",")
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  form = VenueForm(request.form)
  if request.method == 'POST':
      try:
        venue = Venue.query.get(venue_id)

        venue.name = form.name.data
        venue.city = form.city.data
        venue.state = form.state.data
        venue.phone = form.phone.data
        #convert the genres to string in order to save it into the db
        venue.genres=",".join(form.genres.data)
        venue.image_link = form.image_link.data
        venue.facebook_link = form.facebook_link.data
        venue.website_link =  form.website_link.data
        venue.seeking_talent = form.seeking_talent.data
        venue.seeking_desc =  form.seeking_description.data

        db.session.add(venue)
        db.session.commit()

        flash("Record for " + venue.name + "has been updated!")
      except:
        db.session.rollback()
        print(sys.exc_info)
      finally:
        db.session.close()

  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
    error = False
    data = {}
    form =ArtistForm(request.form)
    try: 
      if request.method =="POST":
          name = form.name.data
          city = form.city.data
          state = form.state.data
          phone =  form.phone.data
          genres = ",".join(form.genres.data)
          image_link = form.image_link.data
          facebook_link = form.facebook_link.data
          website_link = form.website_link.data
          seeking_venues = form.seeking_venue.data
          seeking_desc = form.seeking_description.data
          new_artist = Artist(name=name,city=city,state=state,phone=phone,
          genres=genres,image_link=image_link,
          facebook_link=facebook_link,website_link=website_link,
          seeking_venues=seeking_venues,seeking_desc=seeking_desc)
          db.session.add(new_artist)
          db.session.commit()
          data = new_artist
          # TODO: modify data to be the data object returned from db insertion
          # on successful db insert, flash success
          flash('Artist ' + data.name + ' was successfully listed!')
    except:
          db.session.rollback()
          error = True
    finally:
          db.session.close()
    if error:
      flash('An error occurred. Artist ' + data.name + ' could not be listed.')
        # TODO: on unsuccessful db insert, flash an error instead.
        # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    return render_template('pages/home.html', data=data)


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows

  # TODO: replace with real venues data.
  shows = []
  results = Show.query.all()
  show_dict = {}
  for show in results:
    show_dict["venue_id"] =  show.venues.id
    show_dict["venue_name"] = show.venues.name
    show_dict["artist_id"] =  show.artists.id
    show_dict["artist_name"] = show.artists.name
    show_dict["artist_image_link"] =  show.artists.image_link
    show_dict["start_time"] = show.start_time.strftime("%m/%d/%Y, %H:%M:%S")

    shows.append(show_dict)

  return render_template('pages/shows.html', shows=shows)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  error = False
  data = {}
  form = ShowForm(request.form)
  try:
    if request.method == "POST": 
      artist_id = form.artist_id.data
      venue_id = form.venue_id.data
      start_time = form.start_time.data
      show = Show(artist_id=artist_id,
      venue_id=venue_id,
      start_time=start_time)

      db.session.add(show)
      db.session.commit()
      data = show
      
      # on successful db insert, flash success
      flash('Show was successfully listed!')
  except: 
    db.session.rollback()
    error = True
  finally: 
    db.session.close()
  if error:
    flash('An error occurred. Show could not be listed.')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html', data=data)

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
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
