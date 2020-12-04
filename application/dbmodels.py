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
        index=False,
        unique=False,
        nullable=False
    )
    name = db.Column(
        db.String(256),
        index=False,
        unique=False,
        nullable=False
    )
    role = db.Column(
        db.String(6),
        index=False,
        unique=False,
        nullable=False
    )
    group = db.Column(
        db.Integer,
        index=False,
        unique=False,
        nullable=False
    )
