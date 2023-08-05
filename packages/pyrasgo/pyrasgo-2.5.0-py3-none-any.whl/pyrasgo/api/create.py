"""
API Create Functions
"""
from typing import Any, Dict, List, Optional, Union
from urllib import parse

try:
    from typing import Literal  # Only available on 3.8+ directly
except ImportError:
    from typing_extensions import Literal

from pyrasgo.config import MAX_POLL_ATTEMPTS, POLL_RETRY_RATE
from pyrasgo.utils import polling
from pyrasgo import primitives, schemas, errors
from pyrasgo.schemas.offline import OfflineDataset


class Create:
    """
    API Create Class
    """

    def __init__(self):
        from pyrasgo.api import Get
        from pyrasgo.api.connection import Connection
        from pyrasgo.config import get_session_api_key

        api_key = get_session_api_key()
        self.api = Connection(api_key=api_key)
        self._get = Get()

    def metric(
        self,
        name: str,
        dataset_id: int,
        type: str,
        target_expression: str,
        time_grains: List[Literal["HOUR", "DAY", "WEEK", "MONTH", "QUARTER", "YEAR"]],
        time_dimension: str,
        dimensions: List[str],
        filters: Optional[List[schemas.Filter]] = None,
        meta: Optional[Dict[str, str]] = None,
        label: Optional[str] = None,
        description: Optional[str] = None,
    ) -> schemas.Metric:
        """
        Creates and returns a metric on a dataset

        Args:
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
        """
        time_grain_objs = [schemas.metric.TimeGrain[grain] for grain in time_grains]
        metric = schemas.MetricCreate(
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
        )
        try:
            response = self.api._post(
                "/metric", metric.dict(exclude_unset=True, exclude_none=True), api_version=2
            ).json()
            return schemas.Metric(**response)
        except Exception as err:
            raise errors.RasgoResourceException(f"Could not create metric on dataset '{dataset_id}'.") from err

    def transform(
        self,
        *,
        name: str,
        source_code: str,
        type: Optional[str] = None,
        operation_type: Optional[Literal["SQL", "VIZ"]] = "SQL",
        arguments: Optional[List[dict]] = None,
        description: Optional[str] = None,
        tags: Optional[Union[List[str], str]] = None,
        context: Optional[Dict[str, Any]] = None,
        dw_type: Optional[Literal["SNOWFLAKE", "BIGQUERY", "UNSET"]] = None,
    ) -> schemas.Transform:
        """
        Create and return a new Transform in Rasgo
        Args:
            name: Name of the Transform
            source_code: Source code of transform
            type: Type of transform it is. Used for categorization only
            operation_type: Type of operation that will be created by this transform: SQL, VIZ
            arguments: A list of arguments to supply to the transform
                       so it can render them in the UI. Each argument
                       must be a dict with the keys: 'name', 'description', and 'type'
                       values all strings for their corresponding value
            description: Description of Transform
            tags: List of tags, or a tag (string), to set on this dataset
            context: Object used to add context to transforms for client use
            dw_type: DataWarehouse provider: SNOWFLAKE, BIGQUERY or UNSET
                     if not provided, will be set to your current DataWarehouse

        Returns:
            Created Transform obj
        """
        arguments = arguments if arguments else []

        # Init tag array to be list of strings
        if tags is None:
            tags = []
        elif isinstance(tags, str):
            tags = [tags]

        transform = schemas.TransformCreate(
            name=name,
            type=type,
            operation_type=operation_type,
            source_code=source_code,
            description=description,
            tags=tags,
            context=context,
            dw_type=dw_type.upper() if dw_type else None,
        )
        transform.arguments = [schemas.TransformArgumentCreate(**x) for x in arguments]
        response = self.api._post("/transform", transform.dict(), api_version=2).json()
        return schemas.Transform(**response)

    # ----------------------------------
    #  Internal/Private Create Calls
    # ----------------------------------
    def _dataset_from_draft(
        self,
        *,
        dataset_contract: schemas.DatasetPublish,
        timeout: Optional[int] = None,
    ) -> schemas.Dataset:
        """
        Calls Rasgo's API to publish a Dataset from a Draft.

        Args:
            dataset_contract: publish contract to send to the API
            timeout: Approximate timeout for creating the table in seconds. Raise an APIError if the reached
        Returns:
            Dataset object, polled from async API
        """
        resp = self.api._post(
            "/datasets/publish", dataset_contract.dict(exclude_unset=True, exclude_none=True), api_version=2
        ).json()
        status_tracking = schemas.StatusTracking(**resp)

        return polling.poll_dataset_publish(
            connection_obj=self.api,
            max_poll_attempts=MAX_POLL_ATTEMPTS,
            status_tracking_obj=status_tracking,
            timeout=timeout,
            poll_retry_rate=POLL_RETRY_RATE,
        )

    def _dataset_from_offline_schema(
        self,
        dataset_instructions: OfflineDataset,
        verbose: bool = False,
        timeout: int = None,
    ) -> primitives.Dataset:
        """
        Creates a new dataset based on a Rasgo-compliant dict

        Args:
            dataset_dict: a Rasgo-compliant json dict (converted from a yaml file)
        """
        response = self.api._post("/datasets/from-offline-version", dataset_instructions.dict(), api_version=2).json()
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

    def _dataset_from_table(
        self,
        *,
        fqtn: str,
        dataset_contract: schemas.DatasetCreate,
        timeout: Optional[int] = None,
    ) -> schemas.Dataset:
        """
        Calls Rasgo's API to publish a Dataset from a Table.

        Args:
            fqtn: fully-qualified table name
            dataset_publish_in: publish contract to send to the API
            timeout: Approximate timeout for creating the table in seconds. Raise an APIError if the reached
        Returns:
            Dataset object, polled from async API
        """
        resp = self.api._post(
            f"/datasets/async?fqtn={parse.quote(fqtn)}",
            dataset_contract.dict(exclude_unset=True, exclude_none=True),
            api_version=2,
        ).json()
        status_tracking = schemas.StatusTracking(**resp)

        return polling.poll_dataset_publish(
            connection_obj=self.api,
            max_poll_attempts=MAX_POLL_ATTEMPTS,
            status_tracking_obj=status_tracking,
            timeout=timeout,
            poll_retry_rate=POLL_RETRY_RATE,
        )

    def _operation_set_non_async(
        self, operations: List[schemas.OperationCreate], dataset_dependency_ids: List[int]
    ) -> schemas.OperationSet:
        """
        Create an operation set in Rasgo with specified operation
        and input dataset dependencies ids, in a  non-async status
        """
        operation_set_create = schemas.OperationSetCreate(
            operations=operations, dataset_dependency_ids=dataset_dependency_ids, use_custom_sql=False
        )
        response = self.api._post("/operation-sets", operation_set_create.dict(), api_version=2).json()
        return schemas.OperationSet(**response)

    def _operation_set_async(
        self, operations: List[schemas.OperationCreate], dataset_dependency_ids: List[int]
    ) -> schemas.OperationSetAsyncTask:
        """
        Create an operation set in Rasgo with specified operation
        and input dataset dependencies ids
        """
        operation_set_create = schemas.OperationSetCreate(
            operations=operations, dataset_dependency_ids=dataset_dependency_ids, use_custom_sql=False
        )
        response = self.api._post("/operation-sets/async", operation_set_create.dict(), api_version=2).json()
        return schemas.OperationSetAsyncTask(**response)

    def _operation_set(
        self,
        operations: List[schemas.OperationCreate],
        dataset_dependency_ids: List[int],
        async_compute: bool = True,
        async_verbose: bool = False,
    ) -> schemas.OperationSet:
        """
        Create and return an Operation set based on the input
        operations and dataset dependencies

        Set param `async_compute` to False to not create op with async

        Args:
            operations: List of operations to add to operation set.
                         Should be in ordered by time operation added.
            dataset_dependency_ids: Dataset ids to set as a parent for this operation set
            async_compute: Set to False not create op set in async fashion in backend/API
            async_verbose: If creating op set in async mode, set verbose to True to have verbose output

        Returns:
            Created Operation Set
        """
        if async_compute:
            # Submit the task request
            task_request = self._operation_set_async(
                operations=operations, dataset_dependency_ids=dataset_dependency_ids
            )
            operation_set_id = polling.poll_operation_set_async_status(task_request=task_request, verbose=async_verbose)
            return self._get._operation_set(operation_set_id)
        else:
            return self._operation_set_non_async(operations=operations, dataset_dependency_ids=dataset_dependency_ids)
