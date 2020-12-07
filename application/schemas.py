from . import ma
from .dbmodels import User, Territories, Markers, TerritoryCoordinates


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        fields = ("id", "username", "name", "role", "email", "markers", "territory")

    territory = ma.auto_field()
    markers = ma.auto_field()


class CoordinatesSchema(ma.SQLAlchemySchema):
    class Meta:
        model = TerritoryCoordinates
        fields = ("longitude", "latitude")


class TerritoriesSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Territories
        fields = ("id", "name", "description", "coordinates", "user", "markers")

    coordinates = ma.Nested(CoordinatesSchema, many=True)


class MarkersSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Markers
        fields = ("id", "name", "description", "longitude", "latitude", "user", "territory")
