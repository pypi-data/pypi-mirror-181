from typing import List, Optional, Union
from warnings import warn

import arrow

from rhino_health.lib.endpoints.dataschema.dataschema_dataclass import Dataschema, FutureDataschema
from rhino_health.lib.endpoints.endpoint import Endpoint, NameFilterMode, VersionMode
from rhino_health.lib.utils import rhino_error_wrapper


class DataschemaEndpoints(Endpoint):
    """
    @autoapi False
    """

    @property
    def dataschema_data_class(self):
        """
        @autoapi False
        """
        return Dataschema

    @rhino_error_wrapper
    def get_dataschemas(self, dataschema_uids: Optional[List[str]] = None) -> List[Dataschema]:
        """
        @autoapi True
        Gets the Dataschemas with the specified DATASCHEMA_UIDS

        .. warning:: This feature is under development and the interface may change
        """
        warn(
            "The Dataschema dataclass is not fully functional and will be fixed in the near future"
        )
        if not dataschema_uids:
            return self.session.get("/dataschemas/").to_dataclasses(self.dataschema_data_class)
        else:
            return [
                self.session.get(f"/dataschemas/{dataschema_uid}/").to_dataclass(
                    self.dataschema_data_class
                )
                for dataschema_uid in dataschema_uids
            ]


class DataschemaFutureEndpoints(DataschemaEndpoints):
    """
    @objname DataschameEndpoints
    """

    @property
    def dataschema_data_class(self):
        return FutureDataschema

    @rhino_error_wrapper
    def get_dataschema_by_name(
        self, name, version=VersionMode.LATEST, project_uid=None
    ) -> Optional[Dataschema]:
        """
        Returns the latest or a specific Dataschema dataclass

        .. warning:: This feature is under development and the interface may change
        .. warning:: There is no uniqueness constraint on the name for dataschemas so you may not get the correct result
        .. warning:: VersionMode.ALL will return the same as VersionMode.LATEST

        Parameters
        ----------
        name: str
            Full name for the Dataschema
        version: Optional[Union[int, VersionMode]]
            Version of the Dataschema, latest by default, for an earlier version pass in an integer
        project_uid: Optional[str]
            Project UID to search under

        Returns
        -------
        dataschema: Optional[Dataschema]
            Dataschema with the name or None if not found

        Examples
        --------
        >>> session.dataschema.get_dataschema_by_name("My Dataschema")
        Dataschema("My Dataschema")
        """
        if version == VersionMode.ALL:
            warn(
                "VersionMode.ALL behaves the same as VersionMode.LATEST for get_dataschema_by_name(), did you mean to use search_for_dataschemas_by_name()?",
                RuntimeWarning,
            )
        results = self.search_for_dataschemas_by_name(
            name, version, project_uid, NameFilterMode.EXACT
        )
        if len(results) > 1:
            warn(
                "More than one data schema was found with the name for the provided project,"
                "please verify the schema is correct. This function returns the last created schema",
                RuntimeWarning,
            )
        return (
            sorted(results, key=lambda x: arrow.get(x.created_at), reverse=True)[0]
            if results
            else None
        )

    @rhino_error_wrapper
    def search_for_dataschemas_by_name(
        self,
        name: str,
        version: Optional[Union[int, VersionMode]] = VersionMode.LATEST,
        project_uid: Optional[str] = None,
        name_filter_mode: Optional[NameFilterMode] = NameFilterMode.CONTAINS,
    ):
        """
        Returns DataSchema dataclasses

        .. warning:: This feature is under development and the interface may change

        Parameters
        ----------
        name: str
            Full or partial name for the Dataschema
        version: Optional[Union[int, VersionMode]]
            Version of the Dataschema, latest by default
        project_uid: Optional[str]
            Project UID to search under
        name_filter_mode: Optional[NameFilterMode]
            Only return results with the specified filter mode. By default uses CONTAINS

        Returns
        -------
        dataschemas: List[Dataschema]
            Dataschema dataclasses that match the name

        Examples
        --------
        >>> session.dataschema.search_for_dataschemas_by_name("My Dataschema")
        [Dataschema(name="My Dataschema")]

        See Also
        --------
        rhino_health.lib.endpoints.endpoint.FilterMode : Different modes to filter by
        rhino_health.lib.endpoints.endpoint.VersionMode : Return specific versions


        """
        warn(
            "The Dataschema dataclass is not fully functional and will be fixed in the near future"
        )
        query_params = self._get_filter_query_params(
            {"name": name, "version": version, "project_uid": project_uid},
            name_filter_mode=name_filter_mode,
        )
        results = self.session.get("/dataschemas", params=query_params)
        return results.to_dataclasses(self.dataschema_data_class)

    @rhino_error_wrapper
    def create_dataschema(self, dataschema, return_existing=True, add_version_if_exists=False):
        """
        @autoapi False

        Adds a new dataschema

        Parameters
        ----------
        dataschema: FutureDataschema
            FutureDataschema data class
        return_existing: bool
            If a Dataschema with the name already exists, return it instead of creating one.
            Takes precedence over add_version_if_exists
        add_version_if_exists
            If a Dataschema with the name already exists, create a new version.

        Returns
        -------
        dataschema: Dataschema
            Dataschema dataclass

        Examples
        --------
        >>> session.dataschema.create_dataschema(create_dataschema_input)
        Dataschema()

        .. warning:: This feature is under development and incomplete
        """
        # TODO: Change to input subclass as the parameter to be consistent with other endpoints
        raise NotImplementedError(
            "This feature is not yet supported"
        )  # The old code never worked in the first place
        if return_existing or add_version_if_exists:
            try:
                existing_dataschema = self.search_for_dataschemas_by_name(
                    dataschema.name,
                    project_uid=dataschema.project_uid,
                    name_filter_mode=NameFilterMode.EXACT,
                )[0]
                if return_existing:
                    return existing_dataschema
                else:
                    dataschema.base_version_uid = (
                        existing_dataschema.base_version_uid or existing_dataschema.uid
                    )
                    dataschema.__fields_set__.discard("version")
            except Exception:
                # If no existing AI Model exists do nothing
                pass
        result = self.session.post("/dataschemas", dataschema.create_data)
        return result.to_dataclass(self.dataschema_data_class)

    @rhino_error_wrapper
    def get_dataschema_csv(self, dataschema_uid: str):
        """
        @autoapi False

        .. warning:: This feature is under development and incomplete
        """
        return self.session.get(f"/dataschemas/{dataschema_uid}/export_to_csv")

    @rhino_error_wrapper
    def remove_dataschema(self, dataschema_uid: str):
        """
        Removes a Dataschema with the DATASCHAMA_UID from the system
        .. warning:: This feature is under development and incomplete
        """
        return self.session.post(f"/dataschemas/{dataschema_uid}/remove")
