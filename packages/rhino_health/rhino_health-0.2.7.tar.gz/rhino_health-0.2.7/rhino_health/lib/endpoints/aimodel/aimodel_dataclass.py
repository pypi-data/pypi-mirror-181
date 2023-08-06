import json
from enum import Enum
from typing import Any, List, Optional

from pydantic import Field, root_validator
from typing_extensions import Annotated

from rhino_health.lib.dataclass import RhinoBaseModel
from rhino_health.lib.endpoints.endpoint import RESULT_DATACLASS_EXTRA


class ModelTypes(str, Enum):
    """
    Supported AIModel Types
    """

    CLARA_TRAIN = "Clara Train"
    GENERALIZED_COMPUTE = "Generalized Compute"
    NVIDIA_FLARE_V2_0 = "NVIDIA FLARE v2.0"
    NVIDIA_FLARE_V2_2 = "NVIDIA FLARE v2.2"
    PYTHON_CODE = "Python Code"


class AIModelCreateInput(RhinoBaseModel):
    """
    @autoapi True
    """

    name: str
    """@autoapi True The name of the AIModel"""
    description: str
    """@autoapi True The description of the AIModel"""
    version: Optional[int]
    """@autoapi True The version of the AIModel"""
    input_data_schema_uid: Annotated[Optional[str], Field(alias="input_data_schema")]
    """@autoapi True The first data schema uid this ai model expects input cohorts to adhere to"""
    output_data_schema_uid: Annotated[Optional[str], Field(alias="output_data_schema")]
    """@autoapi True The first data schema uid this ai model expects output cohorts to adhere to"""
    input_data_schema_uids: Optional[List[str]]
    """@autoapi True A list of uids of data schemas this ai model expects input cohorts to adhere to. This feature cannot be used in conjunction with the singular version. Only supported by Generalized Compute"""
    output_data_schema_uids: Optional[List[Optional[str]]]
    """@autoapi True A list of uids of data schemas this ai model expects output cohorts to adhere to. This feature cannot be used in conjunction with the singular version. Only supported by Generalized Compute"""
    project_uid: Annotated[str, Field(alias="project")]
    """@autoapi True The AIModel project"""
    model_type: Annotated[str, Field(alias="type")]
    """@autoapi True The model type which corresponds to the ModelTypes enum
    
    See Also
    --------
    rhino_health.lib.endpoints.aimodel.aimodel_dataclass.ModelTypes
    """
    base_version_uid: Optional[str] = ""
    """@autoapi True The first version of the AIModel"""
    config: Optional[dict] = None


class AIModel(AIModelCreateInput, extra=RESULT_DATACLASS_EXTRA):
    """
    @autoapi True
    """

    uid: str
    """@autoapi True The unique ID of the AIModel"""
    created_at: str
    """@autoapi True When this AIModel was added"""
    _project: Any = None
    _input_data_schemas: Any = None
    _output_data_schemas: Any = None

    @property
    def project(self):
        """
        @autoapi True

        Get the project of this AIModel

        .. warning:: Be careful when calling this for newly created objects.
            The project associated with the PROJECT_UID must already exist on the platform.

        .. warning:: The result of this function is cached.
            Be careful calling this function after making changes to the aimodel

        Returns
        -------
        project: Project
            A DataClass representing the Project of the user's primary workgroup

        See Also
        --------
        rhino_health.lib.endpoints.project.project_dataclass : Project Dataclass
        """
        if self._project:
            return self._project
        if self.project_uid:
            self._project = self.session.project.get_projects([self.project_uid])[0]
            return self._project
        else:
            return None

    @property
    def input_data_schemas(self):
        """
        Returns the input data schemas for this AI Model

        .. warning:: The result of this function is cached.
            Be careful calling this function after making changes to the aimodel
        """
        if self._input_data_schemas:
            return self._input_data_schemas
        self._input_data_schemas = self.session.dataschema.get_dataschemas(
            self.input_data_schema_uids
        )

    @property
    def output_data_schemas(self):
        """
        Returns the output data schemas for this AI Model

        .. warning:: The result of this function is cached.
            Be careful calling this function after making changes to the aimodel
        """
        if self._output_data_schemas:
            return self._output_data_schemas
        self._output_data_schemas = self.session.dataschema.get_dataschemas(
            self.output_data_schema_uids
        )


class AIModelRunInputBase(RhinoBaseModel):
    """
    @autoapi False
    Base class for both multi and legacy single cohort run
    """

    def __init__(self, *args, **kwargs):
        run_params = kwargs.get("run_params", None)
        if isinstance(run_params, dict):
            kwargs["run_params"] = json.dumps(run_params)
        secret_run_params = kwargs.get("secret_run_params", None)
        if isinstance(secret_run_params, dict):
            kwargs["secret_run_params"] = json.dumps(secret_run_params)
        super().__init__(*args, **kwargs)

    aimodel_uid: str
    """@autoapi True The unique ID of the AIModel"""
    run_params: Optional[str] = "{}"
    """@autoapi True The run params code you want to run on the cohorts"""
    timeout_seconds: Optional[int] = 600
    """@autoapi True The time before a timeout is declared for the run"""
    secret_run_params: Optional[str]
    """The secrets for the AI model"""
    sync: Optional[bool] = True
    """@autoapi True If True wait for run to end if False let it run in the background"""

    @root_validator
    def passwords_match(cls, values):
        if values.get("sync", True) and values.get("timeout_seconds", 600) > 600:
            raise ValueError(
                "Timeout seconds cannot be greater than 600 when run in synchronous mode"
            )
        return values


class AIModelRunInput(AIModelRunInputBase):
    """
    @autoapi True
    Input parameters for running generalized compute with a single input and output cohort per container, or a non generalized compute model type
    """

    input_cohort_uids: List[str]
    """@autoapi True A list of the input cohort uids"""
    output_cohort_names_suffix: str
    """@autoapi True The suffix given to all output cohorts"""


class AIModelMultiCohortInput(AIModelRunInputBase):
    """
    @autoapi True
    Input parameters for running generalized compute with multiple input and/or output cohorts per container
    """

    input_cohort_uids: List[List[str]]
    """ A list of lists of the input cohort uids.

    [[first_cohort_for_first_run, second_cohort_for_first_run ...], [first_cohort_for_second_run, second_cohort_for_second_run ...], ...] for N runs

    Examples
    --------
    Suppose we have the following AIModel with 2 Input Data Schemas:

    - AI Model 
        + DataSchema 1
        + DataSchema 2

    We want to run the AI Model over two sites: Applegate and Bridgestone

    The user passes in cohort UIDs for Cohorts A, B, C, and D in the following order:
    
    [[Cohort A, Cohort B], [Cohort C, Cohort D]]

    The model will then be run over both sites with the following cohorts passed to generalized compute:
    
    - Site A - Applegate:
        + Cohort A - DataSchema 1
        + Cohort B - DataSchema 2
    - Site B - Bridgestone:
        + Cohort C - DataSchema 1
        + Cohort D - DataSchema 2
    """
    output_cohort_naming_templates: List[str]
    """ A list of string naming templates used to name the output cohorts at each site.
    You can use parameters in each template surrounded by double brackets ``{{parameter}}`` which will
    then be replaced by their corresponding values.

    Parameters
    ----------
    workgroup_name:
        The name of the workgroup the AIModel belongs to.
    workgroup_uid:
        The name of the workgroup the AIModel belongs to.
    model_name:
        The AIModel name
    input_cohort_names.n:
        The name of the nth input cohort, (zero indexed)

    Examples
    --------
    Suppose we have two input cohorts, named "First Cohort" and "Second Cohort"
    and our AIModel has two outputs:

    | output_cohort_naming_templates = [
    |     "{{input_cohort_names.0}} - Train",
    |     "{{input_cohort_names.1}} - Test"
    | ]

    After running Generalized Compute, we will save the two outputs as "First Cohort - Train" and "Second Cohort - Test"
    """


class AIModelTrainInput(RhinoBaseModel):
    """
    @autoapi True
    Input for training an NVFlare AI Model
    """

    aimodel_uid: str
    """The unique ID of the AIModel"""
    input_cohort_uids: List[str]
    """A list of the input cohort uids"""
    validation_cohort_uids: List[str]
    """A list of the cohort uids for validation"""
    validation_cohorts_inference_suffix: str
    """The suffix given to all output cohorts"""
    config_fed_server: str
    """The config for the federated server"""
    config_fed_client: str
    """The config for the federated client"""
    secrets_fed_server: Optional[str]
    """The secrets for the federated server"""
    secrets_fed_client: Optional[str]
    """The secrets for the federated client"""
    timeout_seconds: int
    """The time before a timeout is declared for the run"""
