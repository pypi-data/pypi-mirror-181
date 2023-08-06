"""AiiDA Calculations for the OTE Function Strategy."""
from typing import TYPE_CHECKING

from aiida.engine import calcfunction
from aiida.plugins import DataFactory
from oteapi.plugins import create_strategy, load_strategies

if TYPE_CHECKING:  # pragma: no cover
    from aiida.orm import Dict
    from oteapi.interfaces import IFunctionStrategy

    from execflow.wrapper.data.functionconfig import FunctionConfigData


@calcfunction
def init_function(config: "FunctionConfigData", session: "Dict") -> "Dict":
    """Initialize an OTE Function strategy."""
    load_strategies()

    strategy: "IFunctionStrategy" = create_strategy("function", config.get_dict())
    updated_session = session.get_dict()
    updated_session.update(strategy.initialize(updated_session))
    return DataFactory("core.dict")(updated_session)


@calcfunction
def get_function(config: "FunctionConfigData", session: "Dict") -> "Dict":
    """Get/Execute an OTE Function strategy."""
    load_strategies()

    strategy: "IFunctionStrategy" = create_strategy("function", config.get_dict())
    updated_session = session.get_dict()
    updated_session.update(strategy.get(updated_session))
    return DataFactory("core.dict")(updated_session)
