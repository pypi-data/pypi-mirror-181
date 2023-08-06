"""AiiDA Calculations for the OTE Data Resource Strategy."""
from aiida.engine import calcfunction
from aiida.orm import Dict
from oteapi.models import ResourceConfig
from oteapi.plugins import create_strategy, load_strategies


@calcfunction
def init_dataresource(config: Dict, session: Dict) -> Dict:
    """Initialize an OTE Data Resource strategy."""
    resource_config = ResourceConfig(**config.get_dict())

    load_strategies()

    if resource_config.downloadUrl and resource_config.mediaType:
        # Download strategy
        session_update = create_strategy("download", resource_config).initialize(
            session.get_dict()
        )

        # Parse strategy
        parse_session = session.get_dict()
        parse_session.update(session_update)
        session_update = create_strategy("parse", resource_config).initialize(
            session.get_dict()
        )
    elif resource_config.accessUrl and resource_config.accessService:
        # Resource strategy
        session_update = create_strategy("resource", resource_config).initialize(
            session.get_dict()
        )
    else:
        raise ValueError(
            "Either of the pairs downloadUrl/mediaType and accessUrl/accessService "
            "must be defined in the config."
        )
    return Dict(session_update)


@calcfunction
def get_dataresource(config: Dict, session: Dict) -> Dict:
    """Get/Execute an OTE Data Resource strategy."""
    resource_config = ResourceConfig(**config.get_dict())

    load_strategies()

    if resource_config.downloadUrl and resource_config.mediaType:
        # Download strategy
        session_update = create_strategy("download", resource_config).get(
            session.get_dict()
        )

        # Parse strategy
        parse_session = session.get_dict()
        parse_session.update(session_update)
        session_update = create_strategy("parse", resource_config).get(parse_session)
    elif resource_config.accessUrl and resource_config.accessService:
        # Resource strategy
        session_update = create_strategy("resource", resource_config).get(
            session.get_dict()
        )
    else:
        raise ValueError(
            "Either of the pairs downloadUrl/mediaType and accessUrl/accessService "
            "must be defined in the config."
        )
    return Dict(session_update)
