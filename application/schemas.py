from . import ma
from .dbmodels import User, Territories, Markers, TerritoryCoordinates, Communities


class CommunitiesSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Communities
        fields = ("id", "name", "longitude", "latitude")


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        fields = ("id", "username", "name", "role", "email", "markers", "territory", "community")

    territory = ma.auto_field()
    markers = ma.auto_field()
    community = ma.Nested(CommunitiesSchema)


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
        fields = ("id", "name", "description", "longitude", "latitude", "user", "territory", "type")
