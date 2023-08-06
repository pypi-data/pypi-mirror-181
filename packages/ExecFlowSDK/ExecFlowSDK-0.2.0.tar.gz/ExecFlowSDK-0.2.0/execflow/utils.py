"""Utility functions and classes for usage in ExecFlow."""
# pylint: disable=no-name-in-module,no-self-argument
from typing import TYPE_CHECKING, Dict, List, Union

from oteapi.models import (
    FilterConfig,
    FunctionConfig,
    MappingConfig,
    ResourceConfig,
    TransformationConfig,
)
from pydantic import BaseModel, Field, ValidationError, validator

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Type


class DeclarativeStrategyBase(BaseModel):
    """A mix-in class for standard methods."""

    def get_type(self) -> str:
        """Get the type of strategy."""
        strategy_type = self.__class__.__name__[len("Declarative") :].lower()
        if not hasattr(self, strategy_type):
            raise ValueError(
                f"Cannot determine strategy type from {strategy_type!r}. Note, this "
                "function does not work from the DeclarativeStrategyBase mix-in class "
                "directly!"
            )
        return strategy_type

    def get_name(self) -> str:
        """Get the name of the strategy."""
        return getattr(self, self.get_type())

    def get_config(self) -> "Dict[str, Any]":
        """Get the model as a ready-to-parse config for AiiDA calculations."""
        return self.dict(exclude={self.get_type()})

    def __hash__(self) -> int:
        return hash(repr(self))


class DeclarativeDataResource(DeclarativeStrategyBase, ResourceConfig):
    """Data model for data resource."""

    dataresource: str = Field(
        ...,
        description="Name for the strategy within the declarative pipeline.",
    )


class DeclarativeFilter(DeclarativeStrategyBase, FilterConfig):
    """Data model for filter."""

    filter: str = Field(
        ...,
        description="Name for the strategy within the declarative pipeline.",
    )


class DeclarativeFunction(DeclarativeStrategyBase, FunctionConfig):
    """Data model for function."""

    function: str = Field(
        ...,
        description="Name for the strategy within the declarative pipeline.",
    )


class DeclarativeMapping(DeclarativeStrategyBase, MappingConfig):
    """Data model for mapping."""

    mapping: str = Field(
        ...,
        description="Name for the strategy within the declarative pipeline.",
    )


class DeclarativeTransformation(DeclarativeStrategyBase, TransformationConfig):
    """Data model for transformation."""

    transformation: str = Field(
        ...,
        description="Name for the strategy within the declarative pipeline.",
    )


if TYPE_CHECKING:  # pragma: no cover
    DeclarativeStrategy = Union[
        DeclarativeDataResource,
        DeclarativeFilter,
        DeclarativeFunction,
        DeclarativeMapping,
        DeclarativeTransformation,
    ]


class DeclarativePipeline(BaseModel):
    """Data model for a declarative pipeline."""

    version: int = Field(1, description="The declarative pipeline syntax version.")
    strategies: List[
        Union[
            DeclarativeDataResource,
            DeclarativeFilter,
            DeclarativeFunction,
            DeclarativeMapping,
            DeclarativeTransformation,
        ]
    ] = Field(
        ...,
        description=(
            "List of strategies to be used in the pipeline(s), including their "
            "configuration."
        ),
    )
    pipelines: Dict[str, str] = Field(
        ...,
        description="Dict of the pipeline(s) defined as part of the overall pipeline.",
    )

    @validator("strategies", pre=True, each_item=False)
    def type_cast_strategies(
        cls, value: "List[Dict[str, Any]]"
    ) -> "List[DeclarativeStrategy]":
        """Sort strategies into "correct" types."""
        type_mapping: "Dict[str, Type[DeclarativeStrategy]]" = {
            "dataresource": DeclarativeDataResource,
            "filter": DeclarativeFilter,
            "function": DeclarativeFunction,
            "mapping": DeclarativeMapping,
            "transformation": DeclarativeTransformation,
        }
        type_casted_strategies: "List[DeclarativeStrategy]" = []
        for strategy in value:
            for strategy_type, strategy_cls in type_mapping.items():
                if strategy_type in strategy:
                    try:
                        type_casted_strategies.append(strategy_cls(**strategy))
                    except ValidationError as exc:
                        exc_message = str(exc).replace("\n", "\n  ")
                        raise ValueError(
                            "Strategy cannot be validated as a "
                            f"{strategy_cls.__name__!r}."
                            f"\n  strategy: {strategy}\n  {exc_message}"
                        ) from exc
                    else:
                        break
            else:
                raise ValueError(
                    "Strategy does not define a valid strategy type as key:"
                    f"\n  strategy: {strategy}\n  Valid types: {type_mapping}"
                )
        return type_casted_strategies

    @validator("pipelines")
    def ensure_steps_exist(
        cls, value: "Dict[str, str]", values: "Dict[str, Any]"
    ) -> "Dict[str, str]":
        """Ensure the listed steps in the pipelines exist within the same data model."""
        strategy_names = [
            strategy.get_name() for strategy in values.get("strategies", [])
        ]
        pipeline_names = list(value)
        for name, pipeline in value.items():
            pipeline_parts = [part.strip() for part in pipeline.split("|")]
            if not all(
                part in strategy_names + pipeline_names for part in pipeline_parts
            ):
                raise ValueError(
                    f"Part(s) in {name!r} pipeline not found in the list of strategies"
                    " or pipelines within the declarative pipeline."
                )
        return value

    def _strategy_names(self) -> "List[str]":
        """Utility function to return list of strategy names.

        Returns:
            List of strategy names as given in the declarative pipeline.

        """
        return [strategy.get_name() for strategy in self.strategies]

    def get_strategy(self, strategy_name: str) -> "DeclarativeStrategy":
        """Get a strategy based on its given name.

        Parameters:
            strategy_name: The name given the strategy in the declarative pipeline.

        Returns:
            The declarative strategy model object with the given name.

        """
        for strategy in self.strategies:
            if strategy_name == strategy.get_name():
                return strategy
        raise ValueError(
            f"Strategy {strategy_name!r} does not exist among {self._strategy_names()}"
        )

    def parse_pipeline(self, pipeline: str) -> "List[DeclarativeStrategy]":
        """Resolve a pipeline into its strategy parts.

        Parameters:
            pipeline: Name of the pipeline.

        Returns:
            (Ordered) list of strategies in the pipeline.

        """
        if pipeline not in self.pipelines:
            raise ValueError(
                f"Pipeline {pipeline!r} does not exist among {list(self.pipelines)}"
            )

        parsed_pipeline = []

        pipeline_parts = [part.strip() for part in self.pipelines[pipeline].split("|")]
        for part in pipeline_parts:
            if part in self._strategy_names():
                parsed_pipeline.append(self.get_strategy(part))
            elif part in self.pipelines:
                parsed_pipeline.extend(self.parse_pipeline(part))
            else:
                raise ValueError(
                    f"Could unexpectedly not find part {part!r} in the list of known "
                    "strategy and pipeline names!"
                )
        return parsed_pipeline

    def __hash__(self) -> int:
        return hash(repr(self))
