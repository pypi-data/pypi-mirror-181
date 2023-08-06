"""AiiDA Calculations for the OTE Filter Strategy."""
from typing import TYPE_CHECKING

from aiida.engine import calcfunction
from aiida.orm import Dict
from oteapi.models import FilterConfig
from oteapi.plugins import create_strategy, load_strategies

if TYPE_CHECKING:  # pragma: no cover
    from oteapi.interfaces import IFilterStrategy


@calcfunction
def init_filter(config: Dict, session: Dict) -> Dict:
    """Initialize an OTE Filter strategy."""
    load_strategies()

    filter_config = FilterConfig(**config.get_dict())
    strategy: "IFilterStrategy" = create_strategy("filter", filter_config)
    return Dict(strategy.initialize(session.get_dict()))


@calcfunction
def get_filter(config: Dict, session: Dict) -> Dict:
    """Get/Execute an OTE Filter strategy."""
    load_strategies()

    filter_config = FilterConfig(**config.get_dict())
    strategy: "IFilterStrategy" = create_strategy("filter", filter_config)
    return Dict(strategy.get(session.get_dict()))
