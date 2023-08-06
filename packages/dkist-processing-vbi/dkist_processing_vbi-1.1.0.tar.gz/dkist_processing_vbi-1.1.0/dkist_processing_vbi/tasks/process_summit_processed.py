"""Repackage VBI data already calibrated before receipt at the Data Center."""
import logging

from dkist_processing_common.tasks import WorkflowTaskBase
from dkist_processing_common.tasks.mixin.fits import FitsDataMixin

from dkist_processing_vbi.models.tags import VbiTag


class GenerateL1SummitData(WorkflowTaskBase, FitsDataMixin):
    """
    Task class for updating the headers of on-summit processed VBI data.

    Parameters
    ----------
    recipe_run_id : int
        id of the recipe run used to identify the workflow run this task is part of
    workflow_name : str
        name of the workflow to which this instance of the task belongs
    workflow_version : str
        version of the workflow to which this instance of the task belongs

    """

    record_provenance = True

    def run(self) -> None:
        """
        For all input frames.

            - Add data-dependent SPEC-0214 headers
            - Write out
        """
        # This loop is how we ensure that only completed mosaics get processed.
        with self.apm_task_step("Re-tagging INPUT observe frames as CALIBRATED"):
            for dsps_num in range(1, self.constants.num_dsps_repeats + 1):
                for file_name in self.read(
                    tags=[
                        VbiTag.input(),
                        VbiTag.frame(),
                        VbiTag.task("Observe"),
                        VbiTag.dsps_repeat(dsps_num),
                    ]
                ):
                    self.remove_tags(file_name, VbiTag.input())
                    new_tags = [VbiTag.calibrated(), VbiTag.stokes("I")]
                    self.tag(file_name, tags=new_tags)  # Tags are additive
                    logging.debug(f"Tags after tagging are {self.tags(file_name)}")
