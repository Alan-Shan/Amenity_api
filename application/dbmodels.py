from . import db


class User(db.Model):  # USERS
    __tablename__ = 'users'
    id = db.Column(
        db.String(256),
        primary_key=True
    )
    username = db.Column(
        db.String(64),
        index=True,
        unique=True,
        nullable=False
    )
    password = db.Column(
        db.String(256),
        nullable=False
    )
    name = db.Column(
        db.String(256),
        nullable=False
    )
    email = db.Column(
        db.String(64),
        nullable=False
    )
    role = db.Column(
        db.Boolean(),
        nullable=False
    )
    community = db.Column(
        db.String(256),
        db.ForeignKey('communities.id')
    )
    markers = db.relationship('Markers', cascade="all, delete", backref='users')
    territory = db.relationship('Territories', cascade="all, delete")


class Territories(db.Model):  # TERRITORIES
    __tablename__ = 'territories'
    id = db.Column(
        db.String(256),
        primary_key=True
    )
    name = db.Column(
        db.String(256),
        nullable=False
    )
    description = db.Column(
        db.String(256),
        nullable=False
    )
    user = db.Column(
        db.String(256),
        db.ForeignKey('users.id')
    )
    coordinates = db.relationship('TerritoryCoordinates', cascade="all, delete")
    markers = db.relationship('Markers', cascade="all, delete")


class Markers(db.Model):  # MARKERS
    __tablename__ = 'markers'
    id = db.Column(
        db.String(256),
        primary_key=True
    )
    name = db.Column(
        db.String(256),
        nullable=False
    )
    description = db.Column(
        db.String(1000),
        nullable=False
    )
    longitude = db.Column(
        db.Float(),
        nullable=False
    )
    latitude = db.Column(
        db.Float(),
        nullable=False
    )
    type = db.Column(
        db.Integer(),
        nullable=True
    )

    territory = db.Column(
        db.String(256),
        db.ForeignKey('territories.id', ondelete="CASCADE")
    )
    user = db.Column(
        db.String(256),
        db.ForeignKey('users.id', ondelete="CASCADE")
    )


class TerritoryCoordinates(db.Model):
    __tablename__ = 'coordinates'
    id = db.Column(
        db.String(256),
        primary_key=True
    )
    longitude = db.Column(
        db.Float,
        nullable=False
    )
    latitude = db.Column(
        db.Float,
        nullable=False
    )
    territory = db.Column(
        db.String(256),
        db.ForeignKey('territories.id', ondelete="CASCADE")
    )


class Communities(db.Model):
    __tablename__ = 'communities'

    id = db.Column(
        db.String(256),
        primary_key=True
    )
    name = db.Column(
        db.String(256),
        nullable=False
    )
    longitude = db.Column(
        db.Float,
        nullable=True
    )
    latitude = db.Column(
        db.Float,
        nullable=True
    )

    users = db.relationship('User')
