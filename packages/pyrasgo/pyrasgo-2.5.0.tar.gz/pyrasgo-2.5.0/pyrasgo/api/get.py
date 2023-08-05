"""
API Get Functions
"""
from typing import List, Optional

from pyrasgo import errors, primitives, schemas
from pyrasgo.config import DEFAULT_PAGE_SIZE


class Get:
    """
    API Get Class
    """

    def __init__(self):
        from pyrasgo.api.connection import Connection
        from pyrasgo.config import get_session_api_key

        api_key = get_session_api_key()
        self.api = Connection(api_key=api_key)
        self._dw = None

    def dataset(
        self,
        dataset_id: Optional[int] = None,
        fqtn: Optional[str] = None,
        resource_key: Optional[str] = None,
    ) -> primitives.Dataset:
        """
        Return a Rasgo dataset
        """
        try:
            if dataset_id:
                input_identifier = dataset_id
                response = self.api._get(f"/datasets/{dataset_id}", api_version=2).json()
            elif fqtn:
                input_identifier = fqtn
                response = self.api._get(f"/datasets/match/{fqtn}", api_version=2).json()
            elif resource_key:
                input_identifier = resource_key
                response = self.api._get(f"/datasets/rk/{resource_key}", api_version=2).json()
            if not response:
                raise errors.RasgoResourceException(
                    f"Cannot retrieve dataset identified by {input_identifier}. "
                    "No match found or user does not have permission to access it."
                )
            dataset_schema = schemas.Dataset(**response)

            operation_set_schema = None
            if dataset_schema.dw_operation_set_id:
                response = self.api._get(
                    f"/operation-sets/{dataset_schema.dw_operation_set_id}",
                    api_version=2,
                ).json()
                operation_set_schema = schemas.OperationSet(**response)
            return primitives.Dataset(
                api_dataset=dataset_schema,
                api_operation_set=operation_set_schema,
            )
        except Exception:
            if dataset_id:
                not_found = f"id '{dataset_id!r}'"
            elif fqtn:
                not_found = f"fqtn '{fqtn}'"
            elif resource_key:
                not_found = f"resource key '{resource_key}'"
            raise errors.RasgoResourceException(
                f"Dataset with {not_found} does not exist or this API key does not have access."
            )

    def datasets(
        self,
        include_community: bool = False,
    ) -> List[primitives.Dataset]:
        """
        Return all datasets in Rasgo attached to your organization

        Params
        `include_community` boolean:
            Instructs whether to return Rasgo free datasets
        """
        # Get transforms so we can cache them for use in transforming datasets
        transforms = self.transforms()
        offset = 0

        datasets = []
        while True:
            response = self.api._get(
                f"/datasets?page_size={DEFAULT_PAGE_SIZE}&page_start={offset}"
                f"&include_community={include_community}",
                api_version=2,
            ).json()
            for r in response:
                dataset_schema = schemas.Dataset(**r)
                dataset = primitives.Dataset(
                    api_dataset=dataset_schema,
                    transforms=transforms,
                )
                datasets.append(dataset)
            if len(response) < DEFAULT_PAGE_SIZE:
                break
            offset += DEFAULT_PAGE_SIZE
        return datasets

    def dataset_metrics(self, dataset_id: int) -> List[schemas.Metric]:
        """
        Return a list of metrics belonging to a dataset

        Args:
            dataset_id: Rasgo dataset ID for which to get all metrics
        """
        response = self.api._get(f"/datasets/{dataset_id}/metrics", api_version=2).json()
        return [schemas.Metric(**metric) for metric in response]

    def dataset_offline_version(
        self,
        resource_key: Optional[str],
    ) -> schemas.OfflineDataset:
        target = f"/datasets/{resource_key}/offline-version"
        response = self.api._get(resource=target, api_version=2).json()
        return schemas.OfflineDataset(**response)

    def dataset_py(self, dataset_id: int) -> str:
        """
        Return the pyrasgo code which will create an offline copy
        of a dataset (by ds id)
        """
        return self.api._get(
            f"/datasets/{dataset_id}/export/python",
            api_version=2,
        ).json()

    def draft_datasets(self) -> List[primitives.Dataset]:
        """
        Returns a list of unpublished Datasets
        """
        # Get transforms so we can cache them for use in transforming datasets
        transforms = self.transforms()
        offset = 0
        datasets = []
        while True:
            response = self.api._get(
                f"/operation-sets?page_size={DEFAULT_PAGE_SIZE}&page_start={offset}&draft_only=true",
                api_version=2,
            ).json()
            for op_set in response:
                datasets.append(
                    primitives.Dataset(
                        api_operation_set=schemas.BulkOperationSet(**op_set),
                        transforms=transforms,
                    )
                )
            if len(response) < DEFAULT_PAGE_SIZE:
                break
            offset += DEFAULT_PAGE_SIZE
        return datasets

    def metrics(self, dataset_id: int) -> List[schemas.Metric]:
        """
        Return a list of metrics belonging to a dataset

        Args:
            dataset_id: Rasgo dataset ID for which to get all metrics
        """
        return self.dataset_metrics(dataset_id)

    def transform(self, transform_id: int) -> schemas.Transform:
        """Returns an individual transform"""
        try:
            response = self.api._get(f"/transform/{transform_id}", api_version=1).json()
            return schemas.Transform(**response)
        except Exception as err:
            raise errors.RasgoResourceException(
                f"Transform with id '{transform_id}' does not exist or this API key does not have access."
            ) from err

    def transforms(self, include_community: bool = True) -> List[schemas.Transform]:
        """Returns a list of available transforms"""
        response = self.api._get(f"/transform?include_community={include_community}", api_version=2).json()
        return [schemas.Transform(**r) for r in response]

    def community_transforms(self) -> List[schemas.Transform]:
        response = self.api._get("/transform/community", api_version=1).json()
        return [schemas.Transform(**r) for r in response]

    def user(self):
        response = self.api._get("/users/me", api_version=1).json()
        return schemas.User(**response)

    # ----------------------------------
    #  Internal/Private Get Calls
    # ----------------------------------

    def _dataset_columns(self, dataset_id: int) -> List[schemas.DatasetColumn]:
        """
        Return the dataset columns for a specific dataset

        Args:
            dataset_id: Id of dataset to retrieve columns for
        """
        response = self.api._get(
            f"/dataset-columns/ds/{dataset_id}",
            api_version=2,
        ).json()
        return [schemas.DatasetColumn(**x) for x in response]

    def _operation_set(self, operation_set_id: int) -> schemas.OperationSet:
        """
        Return a Rasgo operation set by id
        """
        response = self.api._get(
            f"/operation-sets/{operation_set_id}",
            api_version=2,
        ).json()
        return schemas.OperationSet(**response)

    def _operation_set_async_status(self, task_id: int) -> schemas.OperationSetAsyncTask:
        """
        Returns the status of an Operation Set creation task by id
        """
        response = self.api._get(
            f"/operation-sets/async/{task_id}",
            api_version=2,
        ).json()
        return schemas.OperationSetAsyncTask(**response)
