from . import ma
from .dbmodels import User, Territories, Markers


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        fields = ("id", "username", "name", "role", "email", "markers", "territory")


class TerritoriesSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Territories
        fields = ("id", "name", "description", "coordinates", "user", "markers")


class MarkersSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Markers
        fields = ("id", "name", "description", "longitude", "latitude", "user", "territory")
