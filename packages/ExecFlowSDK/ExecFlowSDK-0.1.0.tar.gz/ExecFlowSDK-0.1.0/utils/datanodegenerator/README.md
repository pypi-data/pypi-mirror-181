# AiiDA DataNode Generator from SOFT7 (S7) Entities

The DataNode Generator is a jinja2 template that accepts a S7 entity as input.

## Setup

First, you need the SOFT7 (S7) package installed.
This can be done either directly from GitHub:

```shell
pip install git+https://github.com/SINTEF/soft7
```

Or by first cloning the repsitory down and installing it from the local clone:

```shell
git clone https://github.com/SINTEF/soft7
pip install soft7
```

## Example

The following Python script loads a S7-entity and generates an AiiDA DataNode:

```python
from pathlib import Path

from jinja2 import Template
import requests
from s7.pydantic_models.soft7 import SOFT7Entity
import yaml

template_file = Path("aiida_data_gen.py.j2").resolve()
output_file = Path("aiida_exampledatanode.py").resolve()

with requests.get(
    "https://gist.githubusercontent.com/quaat/9dda9d11b3167398afd3952863f737cc/raw/"
    "66f1225623898a45a5101fb53022a8aab7a86c00/demo.yaml"
) as response:
    soft_entity = SOFT7Entity(**yaml.safe_load(response.text))

template = Template(template_file.read_text(encoding="utf-8"))
template.stream(entity=soft_entity).dump(str(output_file))
```
