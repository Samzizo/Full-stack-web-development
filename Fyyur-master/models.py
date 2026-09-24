from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#



# set the venue model

class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String())
    facebook_link = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String()))
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, default = False)
    seeking_description = db.Column(db.String())
    # relationship between Venue and Show
    shows = db.relationship('Show', backref='venues', lazy=True)



    def __repr__(self):
        return f'<Venue Name: {self.name}, City: {self.city}, State: {self.state}>'


    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# set the artist model

class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    city = db.Column(db.String(), nullable=False)
    state = db.Column(db.String(), nullable = False)
    phone = db.Column(db.String())
    genres = db.Column(db.ARRAY(db.String()))
    image_link = db.Column(db.String())
    facebook_link = db.Column(db.String())
    website = db.Column(db.String())
    seeking_venue = db.Column(db.Boolean, default = False)# nullable = False, default = False)
    seeking_description = db.Column(db.String(), nullable = False)
    # relationship between Show and Artist
    shows = db.relationship('Show', backref='artists', lazy=True) 

    def __repr__(self):
      return f'<Artist Name: {self.name}, City: {self.city}, State: {self.state}>'
    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

class Show(db.Model):  
    __tablename__ = 'shows'
    id = db.Column(db.Integer, primary_key = True)
    venue_name = db.Column(db.String())
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'), nullable = False)# set the ForeignKey
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable = False) # set the ForeignKey
    start_time = db.Column(db.DateTime()) 
    artist = db.relationship(  # the relationship between show and venue
            "Artist",
            backref=db.backref('shows_artist', cascade='all, delete'))
    venue = db.relationship( # the relationship between show and artist
        'Venue',
        backref=db.backref('shows_venue', cascade='all, delete'))
