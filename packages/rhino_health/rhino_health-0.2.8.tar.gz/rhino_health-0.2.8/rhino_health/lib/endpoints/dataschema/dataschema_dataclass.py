# import csv
# import io
from typing import List, Optional
from warnings import warn

from pydantic import Field
from typing_extensions import Annotated

from rhino_health.lib.dataclass import RhinoBaseModel
from rhino_health.lib.endpoints.endpoint import RESULT_DATACLASS_EXTRA

# class SchemaVariables:
#     def __init__(self, raw_data):
#         self.raw_data = raw_data
#         fieldnames, parsed_data = self.parse_data(raw_data)
#         self.fieldnames = fieldnames
#         self.parsed_data = parsed_data
#
#     def parse_data(self, raw_data):
#         pass  # TODO
#
#     def to_csv(self, csvfile):
#         with csvfile:
#             writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
#
#             writer.writeheader()
#             for row in self.parsed_data:
#                 writer.writerow(row)
#
#             csvfile.close()
#             return csvfile


class Dataschema(RhinoBaseModel, extra=RESULT_DATACLASS_EXTRA):
    """
    @autoapi False
    """

    uid: Optional[str]
    """@autoapi True The Unique ID of the Dataschema"""
    name: str
    """@autoapi True The name of the Dataschema"""
    description: str
    """@autoapi True The description of the Dataschema"""
    base_version_uid: Optional[str]
    """@autoapi True If this Dataschema is a new version of another Dataschema, the original Unique ID of the base Dataschema."""

    version: Optional[int] = 0
    """@autoapi True The revision of this Dataschema"""
    created_at: str
    """@autoapi True When this Dataschema was created"""
    # schema_variables: SchemaVariables
    num_cohorts: int
    """@autoapi True The number of cohorts using this Dataschema"""
    creator: "User"
    """@autoapi True The creator of this Dataschema"""

    # def __init__(self, schema_variables, **data):
    #     self.schema_variables = SchemaVariables(schema_variables)
    #     super().__init__(**data)


class FutureDataschema(Dataschema):
    """
    @autoapi True
    @objname Dataschema
    """

    project_uids: Annotated[List[str], Field(alias="projects")]
    """@autoapi True A list of UIDs of the projects this data schema is associated with"""
    primary_workgroup_uid: Annotated[str, Field(alias="primary_workgroup")]
    """@autoapi True The UID of the primary workgroup for this data schema"""
    schema_variables: List[dict]
    """@autoapi True A list of schema variables in this data schema"""

    @property
    def projects_uids(self):
        """
        @autoapi False

        .. warning:: This function is deprecated and will be removed in the future, please call project_uids
        """
        warn(
            "DataSchema.projects_uids is deprecated and will be removed in the future, please use project_uids()",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.project_uids

    # @property
    # def create_data(self):
    #     """
    #     @autoapi False
    #     # TODO: Function is incomplete
    #     .. warning:: This feature is under development and incomplete
    #     """
    #     data = self.dict(["name", "description", "base_version_uid"])
    #     data["primary_workgroup"] = self.primary_workgroup_uid
    #     data["projects"] = self.project_uids
    #     schema_variable_file = io.StringIO()
    #     # TODO: Figure out the headers
    #     writer = csv.DictWriter(schema_variable_file, fieldnames=fieldnames)
    #     writer.writeheader()
    #     for row in self.schema_variables:
    #         writer.writerow(row)
    #     data["schema_variables"] = schema_variable_file
    #     return data

    # def create(self):
    #     if self._persisted or self.uid:
    #         raise RuntimeError("Dataschema has already been created")
    #     created_cohort = self.session.cohort.create_dataschema(self)
    #     return created_cohort

    def delete(self):
        if not self._persisted or not self.uid:
            raise RuntimeError("Dataschema has already been deleted")

        self.session.dataschema.remove_dataschema(self.uid)
        self._persisted = False
        self.uid = None
        return self

    # TODO: No existing endpoint for this
    # @property
    # def workgroup(self):
    #     raise NotImplementedError
    #     if self._workgroup:
    #         return self._workgroup
    #     if self.workgroup_uid:
    #         self._workgroup = self.session.workgroup.get_workgroups([self.workgroup_uid])[0]
    #         return self._workgroup
    #     else:
    #         return None


from rhino_health.lib.endpoints.user.user_dataclass import User

Dataschema.update_forward_refs()
FutureDataschema.update_forward_refs()
