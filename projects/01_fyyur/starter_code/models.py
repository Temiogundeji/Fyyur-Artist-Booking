from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask, jsonify, render_template, request, Response, flash, redirect, session, url_for
import datetime
from config import SQLALCHEMY_DATABASE_URI
from flask_moment import Moment

app = Flask(__name__)
app.config.from_object('config')
moment = Moment(app)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey("Artist.id"), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey("Venue.id"), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())

    def __repr__(self):
        return f"<Show id={self.id} artist_id={self.artist_id} venue_id={self.venue_id} start_time={self.start_time}"


      

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500), nullable=False)
    facebook_link = db.Column(db.String(120), nullable=False)
    website_link = db.Column(db.String(120), nullable=True)
    genres = db.Column(db.String(120), nullable=False)
    seeking_talent = db.Column(db.Boolean, nullable=False, default=False)
    seeking_desc = db.Column(db.String, nullable=False)
    shows = db.relationship("Show", backref='venues', lazy=False, cascade="all, delete-orphan")
    created = db.Column(
              db.DateTime, nullable=False,
               default=datetime.datetime.now())
    updated = db.Column(db.DateTime,
               onupdate=datetime.datetime.now())
    # TODO: implement any missing fields, as a database migration using Flask-Migrate


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500), nullable=False)
    facebook_link = db.Column(db.String(120), nullable=False)
    website_link = db.Column(db.String(120), nullable=False)
    seeking_venues = db.Column(db.Boolean, nullable=False, default=False)
    seeking_desc = db.Column(db.String(120), nullable=False)
    shows = db.relationship("Show", backref='artists', lazy=False, cascade="all, delete-orphan")
    created = db.Column(
        db.DateTime, nullable=False,
        default=datetime.datetime.now())
    updated = db.Column(db.DateTime,
        onupdate=datetime.datetime.now())


db.create_all()