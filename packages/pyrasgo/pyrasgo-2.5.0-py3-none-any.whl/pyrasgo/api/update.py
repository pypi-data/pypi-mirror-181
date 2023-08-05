"""
API Update Functions
"""
import logging
import time
from typing import Any, Dict, List, Optional, Union

try:
    from typing import Literal  # Only available on 3.8+ directly
except ImportError:
    from typing_extensions import Literal

from pyrasgo import errors, primitives, schemas
from pyrasgo.config import MAX_POLL_ATTEMPTS, POLL_RETRY_RATE
from pyrasgo.schemas.dataset import Dataset, DatasetRePublish
from pyrasgo.schemas.offline import OfflineDataset
from pyrasgo.utils import polling


class Update:
    """
    API Update Class
    """

    def __init__(self):
        from pyrasgo.api import Get
        from pyrasgo.api.connection import Connection
        from pyrasgo.config import get_session_api_key

        api_key = get_session_api_key()
        self.api = Connection(api_key=api_key)
        self.get = Get()
        self._dw = None

    def dataset(
        self,
        dataset: primitives.Dataset,
        *,
        name: Optional[str] = None,
        description: Optional[str] = None,
        attributes: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None,
        owners: Optional[List[str]] = None,
        verified: Optional[bool] = None,
    ) -> primitives.Dataset:
        """
        Update a dataset name, description, and/or attributes in Rasgo
        """
        # Raise error if trying to update a dataset in offline mode
        if not dataset._api_dataset:
            raise errors.RasgoRuleViolation(
                "Can not update dataset. Needs to be saved first with `rasgo.save.dataset()`"
            )

        if dataset.source_type == "DBT":
            raise errors.RasgoRuleViolation("Can not update datasets sourced from DBT.")

        dataset_update = schemas.DatasetUpdate(
            name=name,
            description=description,
            attributes=attributes,
            tags=tags,
            owner_emails=owners,
            verified=verified,
        )
        response = self.api._put(
            f"/datasets/{dataset._api_dataset.id}",
            dataset_update.dict(exclude_unset=True, exclude_none=True),
            api_version=2,
        ).json()
        dataset_schema = schemas.Dataset(**response)
        return primitives.Dataset(api_dataset=dataset_schema)

    def dataset_column(
        self,
        dataset_column_id: int,
        display_name: Optional[str] = None,
        description: Optional[str] = None,
        attributes: Optional[dict] = None,
    ) -> schemas.DatasetColumn:
        """
        Update metadata about a dataset column

        Args:
            dataset_column_id: Dataset column id to updated. Use `dataset.columns[x].id` to retrieve
            display_name: Display name to update for this dataset column if set
            description: Description to update for this dataset column if set
            attributes: Attributes to add or update for this dataset column. Set as Key Value pairs dict

        Returns:
            Updated Dataset Column Obj
        """
        ds_col_update = schemas.DatasetColumnUpdate(
            id=dataset_column_id,
            display_name=display_name,
            description=description,
            attributes=attributes,
        )
        resp = self.api._put(
            f"/dataset-columns/{dataset_column_id}",
            ds_col_update.dict(exclude_unset=True, exclude_none=True),
            api_version=2,
        ).json()
        return schemas.DatasetColumn(**resp)

    def dataset_table(self, dataset: primitives.Dataset, verbose: bool = False, timeout: Optional[int] = None) -> None:
        """
        Kicks off a query for re-materializing a dataset's set Dw Table.

        The dataset needs to be published first in order call this function

        Args:
            dataset: Published dataset to refresh table for
            verbose: If True will print information related to refreshing table
            timeout: Approximate timeout for creating the table in seconds. Raise an APIError if the reached
        """
        # We need to ensure that the API dataset is exists and is published
        if not dataset._api_dataset:
            raise errors.RasgoRuleViolation("Cannot refresh table. Dataset must first be published")

        if verbose:
            print(f"Refreshing table for dataset with id '{dataset.id}' at fqtn: '{dataset.fqtn}'")

        # Call endpoint to kick off Query to re-create table in worker
        response = self.api._put(f"/datasets/{dataset._api_dataset.id}/table-refresh", api_version=2).json()
        status_tracking = schemas.StatusTracking(**response)

        # Poll the async job until completion, failure, or timeout
        for i in range(1, MAX_POLL_ATTEMPTS):
            status_tracking = schemas.StatusTracking(
                **self.api._get(f"/status-tracking/{status_tracking.tracking_uuid}", api_version=2).json()
            )
            if status_tracking.status == "completed":
                if verbose:
                    print(f"Done Refreshing table for dataset with id '{dataset.id}' " f"at fqtn: '{dataset.fqtn}'")
                break
            if status_tracking.status == "failed":
                raise errors.APIError(f"Could not refresh dataset table: {status_tracking.message}")
            if timeout and (POLL_RETRY_RATE * i) > timeout:
                raise errors.APITimeoutWarning("Timeout reached waiting for dataset table refreshing")
            time.sleep(POLL_RETRY_RATE)
            if verbose:
                print("Query still executing...")

    def dataset_schema(self, dataset_id: int) -> None:
        """
        Queries the information_schema to get column metadata from Snowflake
        Then updates this dataset's column metadata in Rasgo to match
        """
        self.api._put(
            f"/datasets/{dataset_id}/sync-schema",
            api_version=2,
        ).json()

    def metric(
        self,
        metric_id: int,
        dataset_id: Optional[int] = None,
        name: Optional[str] = None,
        type: Optional[str] = None,
        target_expression: Optional[str] = None,
        time_grains: Optional[List[Literal["HOUR", "DAY", "WEEK", "MONTH", "QUARTER", "YEAR"]]] = None,
        time_dimension: Optional[str] = None,
        dimensions: Optional[List[str]] = None,
        filters: Optional[List[schemas.Filter]] = None,
        meta: Optional[Dict[str, str]] = None,
        label: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> schemas.Metric:
        """
        Updates and returns a metric on a dataset

        Args:
            metric_id: Rasgo ID of desired metric to update
            name: Name of the new metric
            dataset_id: Rasgo ID for the dataset the metric will be built from
            type: Aggregate function to create the metric, e.g., "average" or "sum"
            target_expression: Column name or expression on which to create the metric
            time_grains: Time level at which to apply the metric, e.g., "DAY" or "WEEK"
            time_dimension: Name of date/time column on which to apply the time_grains
            dimensions: Other dimensional column names used in metric calculation
            filters: Filter expressions to apply to the dataset before calculating metric values
            meta: Metadata about the metric to store as attributes
            label: For tagging and organization purposes, add labels to your metrics
            description: Explanatory information about your new metric
            tags: List of user-defined strings used to categorize this metric
        """
        time_grain_objs = None
        if time_grains:
            time_grain_objs = [schemas.metric.TimeGrain[grain] for grain in time_grains]
        metric = schemas.MetricUpdate(
            id=metric_id,
            ds_dataset_id=dataset_id,
            name=name,
            type=type,
            target_expression=target_expression,
            time_grains=time_grain_objs,
            time_dimension=time_dimension,
            dimensions=dimensions,
            filters=filters,
            meta=meta,
            label=label,
            description=description,
            tags=tags,
        )
        try:
            response = self.api._put(
                "/metric", metric.dict(exclude_unset=True, exclude_none=True), api_version=2
            ).json()
            return schemas.Metric(**response)
        except Exception as err:
            raise errors.RasgoResourceException(f"Could not update metric with ID '{metric_id}'.") from err

    def transform(
        self,
        transform_id: int,
        name: Optional[str] = None,
        source_code: Optional[str] = None,
        type: Optional[str] = None,
        operation_type: Optional[Literal["SQL", "VIZ"]] = None,
        arguments: Optional[List[dict]] = None,
        description: Optional[str] = None,
        tags: Optional[Union[List[str], str]] = None,
        dw_type: Optional[Literal["SNOWFLAKE", "BIGQUERY", "UNSET"]] = None,
        verified: Optional[bool] = None,
    ) -> schemas.Transform:
        """
        Updates a transform in Rasgo

        Args:
            transform_id: Id of transform to update
            name: Name of the Transform: argument will be deprecated in a future version
            source_code: Source code of transform
            type: Type of transform it is. Used for categorization only
            operation_type: Type of operation this transform will create
            arguments: A list of arguments to supply to the transform
                       so it can render them in the UI. Each argument
                       must be a dict with the keys: 'name', 'description', and 'type'
                       values all strings for their corresponding value
            description: Description of Transform
            tags: List of tags, or a tag (string), to set on this dataset
            dw_type: DataWarehouse provider: SNOWFLAKE, BIGQUERY or UNSET
            verified: Rhe verification status of the transform
        """
        if name:
            logging.warning(
                "Cannot change a transform's name! This argument is deprecated. "
                "It will be ignored in this update and will be removed from this function in a future release. "
                "Please run `rasgo.create.transform()` to create a transform with a different name."
            )

        # Init tag array to be list of strings
        if tags is None:
            tags = []
        elif isinstance(tags, str):
            tags = [tags]

        # Make request to update transform and return
        transform_update = schemas.TransformUpdate(
            type=type,
            operation_type=operation_type,
            description=description,
            source_code=source_code,
            arguments=arguments,
            tags=tags,
            dw_type=dw_type.upper() if dw_type else None,
            verified=verified,
        )
        response = self.api._put(
            f"/transform/{transform_id}",
            transform_update.dict(exclude_unset=True, exclude_none=True),
            api_version=2,
        ).json()
        return schemas.Transform(**response)

    def _dataset_from_offline_schema(
        self,
        dataset_instructions: OfflineDataset,
        verbose: bool = False,
        timeout: int = None,
    ) -> primitives.Dataset:
        """
        Updates a dataset based on a Rasgo-compliant dict

        Args:
            dataset_instructions: a Rasgo-compliant json dict (converted from a yaml file)
        """
        if verbose:
            print(
                f"NOTE: This function is about to send a request to overwrite Dataset {dataset_instructions.resource_key} "
                f"This includes overwriting the SQL definition of {dataset_instructions.fqtn} with the SQL in your dict."
            )
        existing_ds = self.get.dataset(resource_key=dataset_instructions.resource_key)
        if not existing_ds:
            raise errors.RasgoResourceException(
                f"Dataset with resource key {dataset_instructions.resource_key} does not exist."
            )
        response = self.api._post(
            "/datasets/republish/from-offline-version", dataset_instructions.dict(), api_version=2
        ).json()
        if verbose:
            print(f"Request sent to republish Dataset {dataset_instructions.resource_key}, polling for response...")
        status_tracking = schemas.StatusTracking(**response)
        return polling.poll_dataset_publish(
            connection_obj=self.api,
            max_poll_attempts=MAX_POLL_ATTEMPTS,
            status_tracking_obj=status_tracking,
            timeout=timeout,
            poll_retry_rate=POLL_RETRY_RATE,
        )

    def _republish_dataset(
        self,
        resource_key: str,
        dataset_contract: DatasetRePublish,
        save_existing_query: bool = True,
        verbose: bool = False,
        timeout: int = None,
    ) -> Dataset:
        """
        Republish an existing Dataset

        Args:
            resource_key: Rasgo Dataset to update
            dataset_contract: Republish contract
        """
        response = self.api._put(
            f"/datasets/rk/{resource_key}/republish?save_existing_query={save_existing_query}",
            dataset_contract.dict(),
            api_version=2,
        ).json()
        if verbose:
            print(f"Request sent to republish Dataset {resource_key}, polling for response...")
        status_tracking = schemas.StatusTracking(**response)
        return polling.poll_dataset_publish(
            connection_obj=self.api,
            max_poll_attempts=MAX_POLL_ATTEMPTS,
            status_tracking_obj=status_tracking,
            timeout=timeout,
            poll_retry_rate=POLL_RETRY_RATE,
        )
