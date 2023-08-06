"""AiiDA Calculations for the OTE Function Strategy."""
from typing import TYPE_CHECKING

from aiida.engine import calcfunction
from aiida.orm import Dict
from oteapi.models import FunctionConfig
from oteapi.plugins import create_strategy, load_strategies

if TYPE_CHECKING:  # pragma: no cover
    from oteapi.interfaces import IFunctionStrategy


@calcfunction
def init_function(config: Dict, session: Dict) -> Dict:
    """Initialize an OTE Function strategy."""
    load_strategies()

    function_config = FunctionConfig(**config.get_dict())
    strategy: "IFunctionStrategy" = create_strategy("function", function_config)
    return Dict(strategy.initialize(session.get_dict()))


@calcfunction
def get_function(config: Dict, session: Dict) -> Dict:
    """Get/Execute an OTE Function strategy."""
    load_strategies()

    function_config = FunctionConfig(**config.get_dict())
    strategy: "IFunctionStrategy" = create_strategy("function", function_config)
    return Dict(strategy.get(session.get_dict()))
