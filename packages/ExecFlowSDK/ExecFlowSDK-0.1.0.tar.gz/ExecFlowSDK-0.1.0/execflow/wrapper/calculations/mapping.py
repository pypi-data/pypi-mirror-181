"""AiiDA Calculations for the OTE Mapping Strategy."""
from typing import TYPE_CHECKING

from aiida.engine import calcfunction
from aiida.orm import Dict
from oteapi.models import MappingConfig
from oteapi.plugins import create_strategy, load_strategies

if TYPE_CHECKING:  # pragma: no cover
    from oteapi.interfaces import IMappingStrategy


@calcfunction
def init_mapping(config: Dict, session: Dict) -> Dict:
    """Initialize an OTE Mapping strategy."""
    load_strategies()

    mapping_config = MappingConfig(**config.get_dict())
    strategy: "IMappingStrategy" = create_strategy("mapping", mapping_config)
    return Dict(strategy.initialize(session.get_dict()))


@calcfunction
def get_mapping(config: Dict, session: Dict) -> Dict:
    """Get/Execute an OTE Mapping strategy."""
    load_strategies()

    mapping_config = MappingConfig(**config.get_dict())
    strategy: "IMappingStrategy" = create_strategy("mapping", mapping_config)
    return Dict(strategy.get(session.get_dict()))
