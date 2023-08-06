"""sample.payload.100 type"""

from errors import SchemaError
from schemata.sample_payload_base import SamplePayloadBase


class SamplePayload(SamplePayloadBase):
    def check_for_errors(self):
        errors = self.derived_errors() + self.hand_coded_errors()
        if len(errors) > 0:
            raise SchemaError(f"Errors making sample.payload.100  for {self}: {errors}")

    def hand_coded_errors(self):
        return []
