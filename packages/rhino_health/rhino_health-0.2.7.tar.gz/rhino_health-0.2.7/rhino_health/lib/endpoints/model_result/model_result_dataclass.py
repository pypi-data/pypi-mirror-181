from typing import Any, List, Optional, Union

from funcy import flatten
from pydantic import Field
from typing_extensions import Annotated

from rhino_health.lib.dataclass import RhinoBaseModel
from rhino_health.lib.endpoints.endpoint import RESULT_DATACLASS_EXTRA


class ModelResult(RhinoBaseModel, extra=RESULT_DATACLASS_EXTRA):
    uid: str
    """The unique ID of the ModelResult"""
    action_type: str
    """The type of action preformed"""
    status: str
    """The action status"""
    start_time: str
    """The action start time"""
    end_time: Any = None
    """The action end time"""
    _aimodel: Any = None
    _input_cohorts: Any = None
    _output_cohorts: Any = None
    input_cohort_uids: Optional[List[List[str]]]
    """
    A list of cohort uids. Each entry is a list of cohorts corresponding to a dataschema on the ai model
    [[first_cohort_for_first_run, second_cohort_for_first_run ...], [first_cohort_for_second_run, second_cohort_for_second_run ...], ...]
    """
    output_cohort_uids: Optional[List[List[str]]]
    """
    A list of cohort uids. Each entry is a list of of cohorts corresponding to a dataschema on the ai model
    [[first_cohort_for_first_run, second_cohort_for_first_run ...], [first_cohort_for_second_run, second_cohort_for_second_run ...], ...]
    """
    aimodel_uid: Annotated[dict, Field(alias="aimodel")]
    """The relevant aimodel object"""
    result_info: Optional[str]
    """The run result info"""
    results_report: Optional[str]
    """The run result report"""
    report_images: List[Any]
    """The run result images"""
    model_params_external_storage_path: Optional[str]
    """The external storage path"""

    @property
    def aimodel(self):
        if self._aimodel:
            return self._aimodel
        if self.aimodel_uid:
            self._aimodel = self.session.aimodel.get_aimodel(self._aimodel)
            return self._aimodel
        else:
            return None

    @property
    def input_cohorts(self):
        """
        Get the Input Cohorts that were used for this ModelResult
        """
        if self._input_cohorts:
            return self._input_cohorts
        results = []
        for cohort_uid in list(flatten(self.input_cohort_uids)):
            results.append(self.session.cohort.get_cohort(cohort_uid))
        self._input_cohorts = results
        return results

    @property
    def output_cohorts(self):
        """
        Get the Output Cohorts that were used for this ModelResult
        """
        if self._output_cohorts:
            return self._output_cohorts
        results = []
        for cohort_uid in list(flatten(self.output_cohort_uids)):
            results.append(self.session.cohort.get_cohort(cohort_uid))
        self._output_cohorts = results
        return results
