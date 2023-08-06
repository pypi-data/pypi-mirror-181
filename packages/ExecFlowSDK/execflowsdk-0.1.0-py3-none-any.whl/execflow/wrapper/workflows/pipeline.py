"""AiiDA WorkChain for the OTE Pipeline."""
from pathlib import Path
from typing import TYPE_CHECKING

from aiida import orm
from aiida.engine import run_get_node, while_
from aiida.engine.processes.workchains.workchain import WorkChain

from execflow.wrapper import calculations
from execflow.wrapper.data.declarative_pipeline import OTEPipelineData

if TYPE_CHECKING:  # pragma: no cover
    from aiida.engine.processes.workchains.workchain import WorkChainSpec


strategy_calculation_mapping = {
    "DeclarativeDataResource": {
        "init": calculations.init_dataresource,
        "get": calculations.get_dataresource,
    },
    "DeclarativeFilter": {
        "init": calculations.init_filter,
        "get": calculations.get_filter,
    },
    "DeclarativeFunction": {
        "init": calculations.init_function,
        "get": calculations.get_function,
    },
    "DeclarativeMapping": {
        "init": calculations.init_mapping,
        "get": calculations.get_mapping,
    },
    "DeclarativeTransformation": {
        "init": calculations.init_transformation,
        "get": calculations.get_transformation,
    },
}


class OTEPipeline(WorkChain):
    """Run an OTE Pipeline.

    Inputs:
        - **pipeline**
          (:py:class:`~execflow.wrapper.data.declarative_pipeline.OTEPipelineData`,
          :py:class:`aiida.orm.Dict`, :py:class:`aiida.orm.SinglefileData`,
          :py:class:`aiida.orm.Str`) -- The declarative pipeline as an AiiDA-valid
          type. Either as a path to a YAML file or the explicit content of the YAML
          file.

    Outputs:
        - **session** (:py:class:`aiida.orm.Dict`) -- The OTE session object after
          running the pipeline.

    Outline:
        - :py:meth:`~execflow.wrapper.workflows.pipeline.OTEPipeline.setup`
        - while
          :py:meth:`~execflow.wrapper.workflows.pipeline.OTEPipeline.not_finished`:

          - :py:meth:`~execflow.wrapper.workflows.pipeline.OTEPipeline.submit_next`
          - :py:meth:`~execflow.wrapper.workflows.pipeline.OTEPipeline.process_current`

        - :py:meth:`~execflow.wrapper.workflows.pipeline.OTEPipeline.finalize`

    Exit Codes:
        - **2** (*ERROR_SUBPROCESS*) -- A subprocess has failed.

    """

    @classmethod
    def define(cls, spec: "WorkChainSpec") -> None:
        super().define(spec)

        spec.input(
            "pipeline",
            valid_type=(OTEPipelineData, orm.Dict, orm.SinglefileData, orm.Str),
        )
        spec.exit_code(2, "ERROR_SUBPROCESS", message="A subprocess has failed.")

        spec.outline(
            cls.setup,
            while_(cls.not_finished)(cls.submit_next, cls.process_current),
            cls.finalize,
        )
        spec.output("session", valid_type=orm.Dict)

    def setup(self) -> None:
        """Setup WorkChain

        Steps:

        - Initialize context.
        - Parse declarative pipeline.
        - Create a list of strategies to run, explicitly adding `init` and `get`
          CalcFunctions.

        """
        self.ctx.current_id = 0

        if isinstance(self.inputs["pipeline"], (OTEPipelineData, orm.Dict)):
            pipeline = OTEPipelineData(value=self.inputs["pipeline"])
        elif isinstance(self.inputs["pipeline"], orm.SinglefileData):
            pipeline = OTEPipelineData(single_file=self.inputs["pipeline"])
        elif isinstance(self.inputs["pipeline"], orm.Str):
            if Path(self.inputs["pipeline"].value).resolve().exists():
                pipeline = OTEPipelineData(filepath=self.inputs["pipeline"])
            else:
                pipeline = OTEPipelineData(value=self.inputs["pipeline"])

        # Outline pipeline
        # For the moment we can only handle a single defined pipeline
        if not pipeline.pipelines or len(pipeline.pipelines) > 1:
            raise NotImplementedError(
                "Currently there is not way of determining which pipeline to run. "
                "Please only supply a single pipeline in the 'pipelines' object of "
                "the declarative pipeline."
            )
        run_pipeline_name = list(pipeline.pipelines)[0]
        strategies = []
        # Initialization
        for strategy in pipeline.get_strategies(run_pipeline_name, reverse=True):
            strategies.append(
                (
                    strategy_calculation_mapping[strategy.__class__.__name__]["init"],
                    strategy.get_config(),
                )
            )
        # Getting
        for strategy in pipeline.get_strategies(run_pipeline_name):
            strategies.append(
                (
                    strategy_calculation_mapping[strategy.__class__.__name__]["get"],
                    strategy.get_config(),
                )
            )

        self.ctx.strategies = strategies

        self.ctx.ote_session = orm.Dict()

    def not_finished(self) -> bool:
        """Determine whether or not the WorkChain is finished.

        Returns:
            Whether or not the WorkChain is finished based on comparing the current
            strategy index in the list of strategies against the total number of
            strategies.

        """
        return self.ctx.current_id < len(self.ctx.strategies)

    def submit_next(self) -> None:
        """Prepare the current step for submission.

        Run the next strategy's CalcFunction and return its ProcessNode to the context.

        """
        current_id = self.ctx.current_id
        calc_function, strategy_config = self.ctx.strategies[current_id]
        session = self.ctx.ote_session

        self.to_context(
            current=run_get_node(
                calc_function, **{"config": strategy_config, "session": session}
            )[1]
        )

    def process_current(self) -> None:
        """Process the current step's Node.

        Report if the process did not finish OK.
        Retrieve the return session update object, update the session and store it back
        to the context for the next strategy to use.

        """
        if not self.ctx.current.is_finished_ok:
            self.report(
                f"A subprocess failed with exit status {self.ctx.current.exit_status}:"
                f" {self.ctx.current.exit_message}"
            )

        session = self.ctx.ote_session.get_dict()
        session.update(
            self.ctx.current.base.links.get_outgoing()
            .get_node_by_label("result")
            .get_dict()
        )
        self.ctx.ote_session = orm.Dict(session)

        self.ctx.current_id += 1

    def finalize(self) -> None:
        """Finalize the WorkChain.

        Set the 'session' output.
        """
        self.out("session", self.ctx.ote_session)
