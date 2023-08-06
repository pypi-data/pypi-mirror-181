# AiiDA DataNode Generator

## Overview

The ExecFlowSDK code generators are based on the Jinja template engine for Python.
The code generators can generate executable source code from a set of configurations and/or data models.
In some use cases, there is a need to generate AiiDA Data Nodes from existing DLite/SOFT or OSP-Core representations.
The code generators will be able to generate the necessary AiiDA classes for integrating these data models in an AiiDA plugin.
In other cases, there is a need go from existing AiiDA Data Nodes to an external representation, e.g., for external data processing or data documentation, in which case the opposite process is needed.  

## Generating DataNodes

The DataNode Generator is a jinja2 template that accepts a S7 entity
as input.

### Input Entity

```yaml
identity: http://onto-ns.com/entity/v1/demo#a77e5e81-2107-45f9-9dde-1f559d961d0a
description: Demonstration
dimensions:
    N: Number of items

properties:
    lat:
        type: float
        shape: ["N"]
        description: Latitude
        unit: angle
    lon:
        type: float
        shape: ["N"]
        description: Longitude
        unit: angle
```

## JINJA Template

```jinja
"""AiiDA Data Node classe generated from SOFT/DLite data models.

Important:
   These classes are auto-generated and should be checked and updated
   according the needs of the plugin.

"""
from typing import TYPE_CHECKING

from aiida.common.exceptions import ModificationNotAllowed
from aiida.orm import Data

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Optional


class {{ entity.description }}(Data):
    """{{ entity.description }}

    AiiDA DataNode generated from SOFT/DLite datamodels.

    Important:
        This class was auto-generated and should be checked and updated
        according to the needs of the plugin.

    Args:{% for property in entity.properties %}
        {{ property }}: {{ entity.properties[property].description }}{% endfor %}

    """

    def __init__(
        self,{% for property in entity.properties %}
        {{ property }}: "Optional[{{ entity.properties[property].type_.value }}]" = None,{% endfor %}
        **kwargs: "Any",
    ) -> None:
        """
        {{ entity.description }} initialization.
        """
        super().__init__(**kwargs)

        attr_dict = {
{% for property in entity.properties %}            "{{ property }}": {{ property }},
{% endfor %}        }

        self.base.attributes.set_many(attr_dict)

    def _check_setter(self, attrkey: str, value: "Any") -> None:
        """
        Prevents modifications if object has been stored. Otherwise update attributes.
        """
        if self.is_stored:
            raise ModificationNotAllowed(
                "The ResourceConfigData object cannot be modified, "
                "it has already been stored."
            )
        self.base.attributes.set(attrkey, value)
{% for property in entity.properties %}
    @property
    def {{ property }}(self) -> "Optional[{{ entity.properties[property].type_.value }}]":
        """Getter method for {{ property }}

        {{ entity.properties[property].description }}
{% if entity.properties[property].unit %}
        Unit: {{ entity.properties[property].unit }}{% endif %}
        """
        return self.base.attributes.get("{{ property }}")

    @{{ property }}.setter
    def {{ property }}(self, value: "Optional[{{ entity.properties[property].type_.value }}]") -> None:
        """Setter method for {{ property }}

        {{ entity.properties[property].description }}
{% if entity.properties[property].unit %}
        Unit: {{ entity.properties[property].unit }}{% endif %}
        """
        self._check_setter("{{ property }}", value)
{% endfor %}
```

### Code generation Example

The following Python script loads a S7-entity and generates an AiiDA DataNode

```python
import yaml
import requests
from jinja2 import Template
from s7.pydantic_models import Entity

template_file = "aiida_data_gen.txt.j2"
output_file = "aiida_exampledatanode.py"

with requests.get(
    ('https://gist.githubusercontent.com/quaat/9dda9d11b3167398afd3952863f737cc/raw/'
     '66f1225623898a45a5101fb53022a8aab7a86c00/demo.yaml')) as r:
    softEntity = Entity(
        **yaml.safe_load(r.text))

template = Template(
    open(template_file, 'r', encoding='utf-8').read())
template.stream(entity=softEntity).dump(output_file)
```

### Result

The output from the previous script will be a DataNode that can be integrated in an AiiDA plugin

```python
"""AiiDA Data Node classe generated from SOFT/DLite data models.

Important:
   These classes are auto-generated and should be checked and updated
   according the needs of the plugin.

"""
from typing import TYPE_CHECKING

from aiida.common.exceptions import ModificationNotAllowed
from aiida.orm import Data

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Optional


class Demonstration(Data):
    """Demonstration

    AiiDA DataNode generated from SOFT/DLite datamodels.

    Important:
        This class was auto-generated and should be checked and updated
        according to the needs of the plugin.

    Args:
        lat: Latitude
        lon: Longitude

    """

    def __init__(
        self,
        lat: "Optional[float]" = None,
        lon: "Optional[float]" = None,
        **kwargs: "Any",
    ) -> None:
        """
        Demonstration initialization.
        """
        super().__init__(**kwargs)

        attr_dict = {
             "lat": lat,
             "lon": lon,
        }

        self.base.attributes.set_many(attr_dict)

    def _check_setter(self, attrkey: str, value: "Any") -> None:
        """
        Prevents modifications if object has been stored. Otherwise update attributes.
        """
        if self.is_stored:
            raise ModificationNotAllowed(
                "The ResourceConfigData object cannot be modified, "
                "it has already been stored."
            )
        self.base.attributes.set(attrkey, value)

    @property
    def lat(self) -> "Optional[float]":
        """Getter method for lat

        Latitude
        Unit: angle
        """
        return self.base.attributes.get("lat")

    @lat.setter
    def lat(self, value: "Optional[float]") -> None:
        """Setter method for lat

        Latitude
        Unit: angle
        """
        self._check_setter("lat", value)

    @property
    def lon(self) -> "Optional[float]":
        """Getter method for lon

        Longitude
        Unit: angle
        """
        return self.base.attributes.get("lon")

    @lon.setter
    def lon(self, value: "Optional[float]") -> None:
        """Setter method for lon

        Longitude
        Unit: angle
        """
        self._check_setter("lon", value)

```
