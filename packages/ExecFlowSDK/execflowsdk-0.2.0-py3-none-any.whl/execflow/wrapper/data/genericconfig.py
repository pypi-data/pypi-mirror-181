"""Generic OTEAPI Config AiiDA Data Node class."""
from typing import TYPE_CHECKING

from aiida.common.exceptions import ModificationNotAllowed
from aiida.orm import Data

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Dict


class GenericConfigData(Data):
    """Generic class for configuration objects.

    Args:
        configuration (dict): Model-specific configuration options,
            which can either be given as key/value-pairs or set as attributes.
        description (str): A description of the configuration model.

    """

    def __init__(
        self, configuration: "dict[str, Any]", description: str, **kwargs: "Any"
    ) -> None:
        super().__init__(**kwargs)

        attr_dict = {"configuration": configuration, "description": description}

        self.base.attributes.set_many(attr_dict)

    @property
    def configuration(self) -> "dict[str, Any]":
        """Model-specific configuration options, which can either be given as
        key/value-pairs or set as attributes."""
        return self.base.attributes.get("configuration")

    @configuration.setter
    def configuration(self, value: "dict[str, Any]") -> None:
        self.set_attribute("configuration", value)

    @property
    def description(self) -> str:
        """A description of the configuration model."""
        return self.base.attributes.get("description")

    @description.setter
    def description(self, value: str) -> None:
        self.set_attribute("description", value)

    def set_attribute(self, attribute_name: str, value: "Any") -> None:
        """Set an attribute, ensuring the Node is not yet stored.

        Args:
            attribute_name: The name of the attribute to set.
            value: The value of the attribute.

        """
        if self.is_stored:
            raise ModificationNotAllowed(
                f"The {self.__class__.__name__} object cannot be modified, "
                "it has already been stored."
            )

        self.base.attributes.set(attribute_name, value)

    def get_dict(self) -> "Dict[str, Any]":
        """Return all attributes as a Python dictionary."""
        return dict(self.base.attributes.all)
