class SchemaError(Exception):
    """Base class for Schema errors"""

    pass


class UnknownSchemaError(Exception):
    """Schema type does not exist or is not recognized"""

    pass


class AlgoError(Exception):
    """Base class for errors related to Algorand"""

    pass


class AlgoErrorBadAddressFormat(Exception):
    """Base class for errors related to Algorand"""

    pass


class DcError(Exception):
    """Base class for dataclass errors"""

    pass


class DjangoError(Exception):
    """Base class for errors related to Django"""

    pass


class DataClassLoadingError(Exception):
    """Base class for errors where a data class object referenced by
    id is not in the local data class dictionary yet. For example
    a primary_component has a component_attribute_class_id but
    the component_attribute_class is not yet in memory"""


class RegistryError(Exception):
    """Base class for errors in making or updating Registry objects (i.e.,
    BaseGNodes and/or GpsPoints"""

    pass
