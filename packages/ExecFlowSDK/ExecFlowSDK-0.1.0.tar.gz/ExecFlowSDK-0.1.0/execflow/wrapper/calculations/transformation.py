"""AiiDA Calculations for the OTE Transformation Strategy."""
from time import sleep, time
from typing import TYPE_CHECKING

from aiida.engine import calcfunction
from aiida.orm import Dict
from oteapi.models import TransformationConfig
from oteapi.plugins import create_strategy, load_strategies

if TYPE_CHECKING:  # pragma: no cover
    from oteapi.interfaces import ITransformationStrategy
    from oteapi.models import TransformationStatus


@calcfunction
def init_transformation(config: Dict, session: Dict) -> Dict:
    """Initialize an OTE Transformation strategy."""
    load_strategies()

    transformation_config = TransformationConfig(**config.get_dict())
    strategy: "ITransformationStrategy" = create_strategy(
        "transformation", transformation_config
    )
    return Dict(strategy.initialize(session.get_dict()))


@calcfunction
def get_transformation(config: Dict, session: Dict) -> Dict:
    """Get an OTE Transformation strategy.

    Important:
        Currently, the status values are valid only for Celery.

        This is because only a single transformation strategy exists (for Celery) and
        the configuration and status models have been based on this strategy.

        A status enumeration should be set as the type for
        `TransformationStatus.status` in order to more agnostically determine the state
        from any transformation strategy.

        However, this is to be implemented in OTEAPI Core.

    """
    load_strategies()

    transformation_config = TransformationConfig(**config.get_dict())
    strategy: "ITransformationStrategy" = create_strategy(
        "transformation", transformation_config
    )

    wall_time = 2 * 60  # 2 min.

    start_time = time()
    status: "TransformationStatus" = strategy.run(session.get_dict())
    while (
        status.status
        not in (
            "READY_STATES",
            "EXCEPTION_STATES",
            "PROPAGATE_STATES",
            "SUCCESS",
            "FAILURE",
            "REVOKED",
            "RETRY",
        )
        or not status.finishTime
    ) and (time() - start_time) < wall_time:
        sleep(0.5)
        status = strategy.status(status.id)

    return Dict(strategy.get(session.get_dict()))
