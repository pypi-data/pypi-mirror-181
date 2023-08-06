""" GpsPoint Base Class Definition """

from typing import Dict
from typing import Optional

from gnf.data_classes.mixin import StreamlinedSerializerMixin
from gnf.errors import DcError


class GpsPoint(StreamlinedSerializerMixin):
    by_id = {}

    def __new__(cls, gps_point_id, *args, **kwargs):
        try:
            return cls.by_id[gps_point_id]
        except KeyError:
            instance = super().__new__(cls)
            cls.by_id[gps_point_id] = instance
            return instance

    def __init__(
        self,
        gps_point_id: Optional[str] = None,
        lat: Optional[float] = None,
        lon: Optional[float] = None,
    ):
        self.gps_point_id = gps_point_id
        self.lat = lat
        self.lon = lon

    def __repr__(self):
        rs = f"GpsPoint lat: {self.lat}, lon: {self.lon} \r gps_point_id: {self.gps_point_id}"

    @classmethod
    def _creation_axiom_1(cls, attributes: Dict):
        """Creation Axiom 1: gps_point_id, lat, lon must all exist"""
        if not "gps_point_id" in attributes.keys():
            raise DcError("gps_point_id must exist")
        if not "lat" in attributes.keys():
            raise DcError("lat must exist")
        if not "lon" in attributes.keys():
            raise DcError("lon must exist")

    @classmethod
    def _creation_axiom_2(cls, attributes: Dict):
        """Creation Axiom 1: lat and lon are both floats"""
        if not isinstance(attributes["lat"], float):
            raise DcError("lat must have type float")
        if not isinstance(attributes["lon"], float):
            raise DcError("lon must have type float")

    @classmethod
    def check_creation_axioms(cls, attributes):
        GpsPoint._creation_axiom_1(attributes)
        GpsPoint._creation_axiom_2(attributes)

    def _update_axiom_1(self, new_attributes):
        """Update Axiom 1: gps_point_id, lat, lon are all immutable"""
        if new_attributes["gps_point_id"] != self.gps_point_id:
            raise DcError("gps_point_id is Immutable")
        if new_attributes["lat"] != self.lat:
            raise DcError("lat is Immutable")
        if new_attributes["lon"] != self.lat:
            raise DcError("lon is Immutable")

    def check_update_axioms(self, new_attributes):
        self._update_axiom_1(new_attributes)
