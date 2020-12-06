import json
from dataclasses import dataclass

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
    markers = db.relationship('Markers')
    territory = db.relationship('Territories')


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
    coordinates = db.relationship('TerritoryCoordinates')
    user = db.Column(
        db.String(256),
        db.ForeignKey('users.id')
    )
    markers = db.relationship('Markers')


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
    territory = db.Column(
        db.String(256),
        db.ForeignKey('territories.id')
    )
    user = db.Column(
        db.String(256),
        db.ForeignKey('users.id')
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
        db.ForeignKey('territories.id')
    )
