"""
Dataset 'Primitive' In Rasgo SDK
"""
from __future__ import annotations
import functools
import inspect
from datetime import datetime
from inspect import Parameter
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple, Union
from pyrasgo.schemas import user as user_schemas


import pandas as pd

from pyrasgo import errors
from pyrasgo.api.connection import Connection
from pyrasgo.constants import SOURCE_TABLE_ARG_NAME, TABLE_ARG_TYPE, TABLE_LIST_ARG_TYPE
from pyrasgo.schemas import (
    OperationSet,
    Dataset as DatasetSchema,
    OperationCreate,
    Transform,
    DatasetColumn,
)
from pyrasgo.storage.datawarehouse import dw_connection
from pyrasgo.utils import naming

__all__ = ['Dataset']


def require_published(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        self: Dataset = args[0]
        self._assert_is_published()
        return func(*args, **kwargs)

    return wrapper


def require_operations(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        self: Dataset = args[0]
        self._assert_has_operations()
        return func(*args, **kwargs)

    return wrapper


class Dataset(Connection):
    """
    Representation of a Rasgo Dataset
    """

    def __init__(
        self,
        # Args passed from Rasgo
        api_dataset: Optional[DatasetSchema] = None,
        api_operation_set: Optional[OperationSet] = None,
        # Args passed from transforming
        operations: Optional[List[OperationCreate]] = None,
        dataset_dependencies: Optional[List[int]] = None,
        table_name: Optional[str] = None,
        transforms: Optional[List[Transform]] = None,
        verbose=False,
        **kwargs: Dict,
    ):
        """
        Init functions in two modes:
            1. This Dataset retrieved from Rasgo. This object is for reference, and cannot
               be changed, but can be transformed to build new datasets
            2. This Dataset represents a new dataset under construction. It is not persisted in Rasgo
               and instead consists of some operations that will be used to generate a new dataset.
        """
        super().__init__(**kwargs)

        self._verbose = verbose
        self._api_dataset: DatasetSchema = api_dataset
        self._api_operation_set: OperationSet = api_operation_set
        self._operations = operations or []
        self._dataset_dependencies = dataset_dependencies or []
        self._table_name = table_name
        if transforms:
            self._available_transforms = transforms
        else:
            self._available_transforms = _get_transforms()

        #  alias .transform allowing direct referencing of named transforms
        for transform in self._available_transforms:
            f = self._create_transform_function(transform)
            setattr(self, transform.name, f)

    def __repr__(self) -> str:
        """
        Get string representation of this dataset
        """
        if self._api_dataset:
            return (
                f"Dataset(id={self.id}, "
                f"name={self.name}, "
                f"resource_key={self._api_dataset.resource_key}, "
                f"fqtn={self.fqtn}, "
                f"verified={self.verified})"
            )
        elif self._api_operation_set and not self._api_operation_set.is_published:
            return (
                f"Draft Dataset(draft_id={self._api_operation_set.id}, "
                f"name={self._api_operation_set.name}, "
                f"draft_resource_key={self._api_operation_set.resource_key}, "
                f"fqtn=N/A, "
                f"verified=N/A)"
            )
        else:
            return "Dataset()"

    # -------------------
    # Properties
    # -------------------

    @property
    def _status(self) -> str:
        """
        Describes the status of the Dataset primitive
        """
        # Dataset record present in API
        if self._api_dataset:
            if not self._api_operation_set:
                self._refresh()
            if self._api_operation_set.is_published:
                return "PUBLISHED DATASET"
            else:
                return "DRAFT DATASET"
        # Dataset record not present in API
        elif self._api_operation_set:
            return "API DRAFT"
        # Dataset record not yet registered
        else:
            return "OFFLINE DRAFT"

    @property
    def attributes(self) -> Optional[Dict]:
        """
        Return the attributes for this dataset if it is from the API
        """
        if self._api_dataset:
            return self._api_dataset.attributes
        elif self._api_operation_set:
            return self._api_operation_set.attributes

    @property
    def columns(self) -> Optional[List[DatasetColumn]]:
        """
        Return the columns for this dataset if it is from the API
        """
        from pyrasgo.api import Get, Read

        if self._status in ("API DRAFT", "OFFLINE DRAFT", "DRAFT DATASET"):
            column_response = []
            schema = Read().data_warehouse.get_schema(self.sql)
            for k, v in schema.items():
                column_response.append(DatasetColumn(name=k, data_type=v))
            return column_response
        else:
            if not self._api_dataset.columns:
                self._api_dataset.columns = Get()._dataset_columns(self.id)
            return self._api_dataset.columns

    @property
    def created_date(self) -> Optional[datetime]:
        """
        Return date this dataset was created
        """
        if self._api_dataset:
            return self._api_dataset.create_timestamp

    @property
    def dependencies(self) -> List[Dataset]:
        """
        Return a list of dataset dependencies for this dataset
        """
        from pyrasgo.api import Get

        dataset_deps = []
        self._refresh()
        dependencies = (
            self._api_operation_set.dataset_dependencies if self._api_operation_set else self._dataset_dependencies
        )
        for ds in dependencies:
            # Class built from a BulkOperationSet will have a list of ids
            if isinstance(ds, int):
                dataset_deps.append(Get().dataset(ds))
            # Class built from an OperationSet will have a list of Datasets
            else:
                dataset_deps.append(Get().dataset(ds.id))
        return dataset_deps

    @property
    def description(self) -> Optional[str]:
        """
        Return dataset description if set/saved
        """
        if self._api_dataset:
            return self._api_dataset.description
        elif self._api_operation_set:
            return self._api_operation_set.description

    @property
    def fqtn(self) -> str:
        """
        Returns the Fully Qualified Table Name for this dataset
        """
        if self._api_dataset:
            return self._api_dataset.fqtn
        elif self._table_name:
            dw_namespace = self._default_dw_namespace()
            return f"{dw_namespace['database']}.{dw_namespace['schema']}.{self._table_name}"
        else:
            raise AttributeError("No fqtn exists for this Dataset")

    @property
    def id(self) -> Optional[int]:
        """
        Return the id for this dataset

        Raise API error if one doesn't exist yet and is an offline dataset
        """
        if self._api_dataset:
            return self._api_dataset.id

    @property
    def is_source(self) -> bool:
        """
        Is this Dataset a standalone source? i.e. does it have no applied operations?
        Sources are imported from csvs, dataframes or directly from Snowflake tables

        This property is a convenience calc to support exporting Datasets to dbt
        """
        if self._api_dataset:
            return self._api_dataset.is_source

    @property
    def name(self) -> Optional[str]:
        """
        Return dataset name if set/saved
        """
        if self._api_dataset:
            return self._api_dataset.name
        elif self._api_operation_set:
            return self._api_operation_set.name

    @property
    def owners(self) -> Optional[List[str]]:
        """
        Return dataset owners if set/saved
        """
        if self._api_dataset:
            return [owner.email for owner in self._api_dataset.owners]

    @property
    def resource_key(self) -> Optional[str]:
        """
        Return the resource key for this dataset.

        Only published datasets will contain this value
        """
        if self._api_dataset:
            return self._api_dataset.resource_key

    @property
    def schema(self) -> Optional[List[Tuple[str, str]]]:
        """
        Return Dataset Schema as list of List of Tuples like (<Col Name>, <Col Data Type>)
        """
        if self._api_dataset:
            data_warehouse = dw_connection(self._dw_type())
            return data_warehouse.list_table_columns(self._api_dataset.fqtn)

    @property
    def source_type(self) -> Optional[str]:
        """
        Return dataset source type if set on published Dataset

        All offline datasets are of type `RASGO`
        """
        if self._api_dataset:
            return self._api_dataset.source_type
        else:
            return "RASGO"

    @property
    def sql(self) -> Optional[str]:
        """
        Return the source code SQL used to generate this dataset
        """
        if self._api_operation_set:
            return self._api_operation_set.sql
        return self._get_cte_for_dataset()

    @property
    def sql_alias(self) -> str:
        """
        Returns an alias for this dataset to use in SQL statements
        Published Dataset: return fqtn
        Draft Dataset: return CTEalias
        """
        if self._api_dataset:
            return self._api_dataset.fqtn
        elif self._table_name:
            return self._table_name
        else:
            raise AttributeError("No sql_alias exists for this Dataset")

    @property
    def table_type(self) -> Optional[str]:
        """
        If this is a published dataset, return the
        table type for it's set Dw Table ( 'VIEW' or 'TABLE')
        """
        if self._api_dataset:
            return self._api_dataset.table_type
        return "VIEW"

    @property
    def tags(self) -> Optional[List[str]]:
        """
        Return dataset tags if set/saved
        """
        if self._api_dataset:
            return self._api_dataset.tags
        elif self._api_operation_set:
            return self._api_operation_set.tags

    @property
    def update_date(self) -> Optional[datetime]:
        """
        Return date this dataset was updated
        """
        if self._api_dataset:
            return self._api_dataset.update_timestamp

    @property
    def verified(self) -> bool:
        return bool(self._api_dataset and self._api_dataset.verified_user)

    @property
    def verified_user(self) -> Optional[user_schemas.NestedUser]:
        if self._api_dataset:
            return self._api_dataset.verified_user.email

    @property
    def verified_timestamp(self) -> Optional[datetime]:
        if self._api_dataset:
            return self._api_dataset.verified_timestamp

    # --------
    # Methods
    # --------

    @require_published
    def dw_sync(self) -> None:
        """
        Looks up the schema of this Dataset's table in the DataWarehouse and synchronizes
        the Dataset's column metadata to match it

        Helpful to pick up common changes:
        - new fields added to table
        - existing fields removed from table
        - data type changes

        Does not pick up:
        - table renames
        - column renames

        Dataset must be published in Rasgo first before you can call this func.
        """
        from pyrasgo.api import Update

        Update().dataset_schema(self.id)
        self._refresh()

    def generate_py(self) -> str:
        """
        Generate and return as a string the PyRasgo code which
        will create an offline a copy of this dataset.

        Dataset must be published in Rasgo first before you can call this func.
        """
        from pyrasgo.api import Get

        return Get().dataset_py(self.id)

    def generate_yaml(self, file_path: Optional[Path] = None) -> str:
        """
        Return a YAML representation of this dataset

        Args:
            file_path: str: full path + file name of the yaml file to write to
        """
        from pyrasgo.api import Get

        ds_schema = Get().dataset_offline_version(self.resource_key)
        if file_path:
            with open(file_path, "w") as yaml_file:
                yaml_file.write(ds_schema.yaml())
            print(f"Dataset version written to yaml file at: {file_path}")
        return ds_schema.yaml()

    def preview(
        self,
        filters: Optional[List[str]] = None,
        order_by: Optional[List[str]] = None,
        columns: Optional[List[str]] = None,
    ) -> pd.DataFrame:
        """
        Preview the first 10 rows of this dataset, returned as pandas dataframe

        You can supply SQL WHERE clause filters, order the dataset by columns, and
        only return selected columns

        Example:
            ```
            ds = rasgo.get.dataset(dataset_id=74)
            ds.preview(
                filters=['SALESTERRITORYKEY = 1', 'TOTALPRODUCTCOST BETWEEN 1000 AND 2000'],
                order_by=['TOTALPRODUCTCOST'],
                columns=['PRODUCTKEY', 'TOTALPRODUCTCOST', 'SALESTERRITORYKEY']
            )
            ```

        Args:
            filters: List of SQL WHERE filters strings to filter on returned df
            order_by: List of columns to order by in returned dataset
            columns: List of columns to return in the df
        """
        return self.to_df(filters, order_by, columns, limit=10)

    @require_published
    def refresh_table(self, verbose: bool = False, timeout: Optional[int] = None) -> None:
        """
        Kicks off a query for re-materializing this dataset's set Dw Table.

        The dataset needs to be published first in order call this function

        Args:
            verbose: If True will print information related to refreshing table
            timeout: Approximate timeout for creating the table in seconds.
                     Raise an APIError if timeout reached

        Dataset must be published in Rasgo first before you can call this func.
        """
        from pyrasgo.api.update import Update

        Update().dataset_table(dataset=self, verbose=verbose, timeout=timeout)

    def to_df(
        self,
        filters: Optional[List[str]] = None,
        order_by: Optional[List[str]] = None,
        columns: Optional[List[str]] = None,
        limit: Optional[int] = None,
    ) -> pd.DataFrame:
        """
        Reads and returns this dataset into a pandas dataframe

        You can supply SQL WHERE clause filters, order the dataset by columns, only
        return selected columns, and add a return limit as well

        Example:
            ```
            ds = rasgo.get.dataset(dataset_id=74)
            ds.to_df(
                filters=['SALESTERRITORYKEY = 1', 'TOTALPRODUCTCOST BETWEEN 1000 AND 2000'],
                order_by=['TOTALPRODUCTCOST'],
                columns=['PRODUCTKEY', 'TOTALPRODUCTCOST', 'SALESTERRITORYKEY'],
                limit=50
            )
            ```

        Args:
            filters: List of SQL WHERE filters strings to filter on returned df
            order_by: List of columns to order by in returned dataset
            columns: List of columns to return in the df
            limit: Only return this many rows in the df
        """
        from pyrasgo.api import Read
        from pyrasgo.utils.rendering import offline_operations_as_cte

        if self._status == "API DRAFT":
            sql = self._api_operation_set.sql
            sql = _add_statements_to_sql(sql, filters, order_by, limit)
            return Read().data_warehouse.query_into_dataframe(sql)

        if self._operations:
            sql = offline_operations_as_cte(operations=self._operations, transforms=self._available_transforms)
            sql = _add_statements_to_sql(sql, filters, order_by, limit)
            if columns:
                final_op_name = self._table_name or naming.gen_operation_table_name(
                    op_num=len(self._operations) + 1,
                    transform_name='drop_columns',
                )
                sql = f"WITH {final_op_name} AS ({sql}) SELECT {','.join(columns)} FROM {final_op_name}"
            return Read().data_warehouse.query_into_dataframe(sql)
        return Read().dataset(
            dataset=self,
            filters=filters,
            order_by=order_by,
            columns=columns,
            limit=limit,
        )

    def to_sql(self) -> Optional[str]:
        """
        Return the SQL statement to create this dataset
        """
        return self.sql

    def transform(
        self,
        transform_name: str,
        arguments: Optional[Dict[str, Union[str, int, List, Dict, Dataset]]] = None,
        operation_name: Optional[str] = None,
        sql_alias: Optional[str] = None,
        **kwargs: Union[str, int, List, Dict, Dataset],
    ) -> Dataset:
        """
        Transform a new dataset with the given transform and arguments.
        Created operation is added to the dataset's canvas/operations set

        Args:
            transform_name: Name of transform to Apply
            arguments: Optional transform arguments sin not supplied by **kwargs
            operation_name: Name to set for the operation/transform
            sql_alias: Alias for this operation when it is rendered as SQL
            **kwargs:

        Returns:
             Returns an new dataset with the referenced transform
             added to this dataset's definition/operation set
        """
        # Update the Transform arguments with any supplied kwargs
        arguments = arguments if arguments else {}
        arguments.update(kwargs)

        # Do any validation on input transform args
        transform = self._get_transform_by_name(transform_name)
        _assert_value_types_of_args(transform, arguments, self)

        # Add required reference to self in transform
        arguments[SOURCE_TABLE_ARG_NAME] = self

        # Scan through supplied transform arguments
        #
        # Determine what should be set for this operation's plus offline dataset's
        # dependencies, along with getting the parent operations for this operation
        # by reading data from input Datasets obj attribute data
        #
        # We also convert 'Datasets' to fqtns in the arguments dict in
        # the func below
        op_deps, ds_deps, parent_ops, arguments = self._get_op_deps_parents_and_args(arguments)

        if not sql_alias:
            # Init table name for outputted dataset
            sql_alias = naming.gen_operation_table_name(
                op_num=len(parent_ops) + 1,
                transform_name=transform_name,
            )

        # Init New Operation Create Contract
        operation_create = OperationCreate(
            operation_name=operation_name if operation_name else transform.name,
            operation_args=arguments,
            transform_id=transform.id,
            sql_alias=sql_alias,
        )

        # Init and return new offline dataset
        return self.__class__(
            operations=parent_ops + [operation_create],
            dataset_dependencies=ds_deps,
            table_name=sql_alias,
        )

    # ---------------------------------
    #  Private Helper Funcs for Class
    # ---------------------------------

    def _refresh(self) -> None:
        """
        Refresh this Dataset's metadata from the Rasgo API
        """
        if self.id:
            self._api_dataset = DatasetSchema(**self._get(f"/datasets/{self.id}", api_version=2).json())
        if self._api_dataset:
            self._api_operation_set = OperationSet(
                **self._get(f"/operation-sets/{self._api_dataset.dw_operation_set_id}", api_version=2).json()
            )

    def _get_cte_for_dataset(self) -> str:
        """
        Return the SQL statement to create this dataset as a CTE
        """
        from pyrasgo.utils.rendering import operations_as_cte, offline_operations_as_cte

        # Need to pull the operation set in case this Dataset was sourced from a bulk contract
        if not self._api_operation_set or not self._api_operation_set.operations:
            self._refresh()
        # If this is an Online Dataset with operations:
        if self._api_operation_set and self._api_operation_set.operations:
            return operations_as_cte(self._api_operation_set.operations)
        # If this is a published Dataset without operations:
        if self._api_dataset:
            return f'SELECT * FROM {self._api_dataset.fqtn}'
        # If this is an Offline Dataset:
        # For now: return None | Future: build an offline CTE rendering function
        else:
            return offline_operations_as_cte(operations=self._operations, transforms=self._available_transforms)

    def _get_transform_by_name(self, transform_name: str) -> Transform:
        """
        Get and return a transform obj by name

        Raise Error if no transform with that name found
        """
        for transform in self._available_transforms:
            if transform_name == transform.name:
                return transform
        raise errors.RasgoResourceException(f"No Transform with name '{transform_name}' available to your organization")

    def _assert_is_created(self) -> None:
        """
        Raise an error if the dataset is not created in Rasgo
        """
        if not self._api_dataset:
            raise errors.RasgoRuleViolation("Dataset must be registered with Rasgo order to perform this action.")

    def _assert_is_published(self) -> None:
        """
        Raise an error if the dataset is not published
        """
        published = True
        if self._api_dataset and not self._api_dataset.fqtn:
            published = False
        if self._api_operation_set and not self._api_operation_set.is_published:
            published = False
        if not published:
            raise errors.RasgoRuleViolation(
                "Dataset must be published in order to perform this action. Please publish your dataset to continue."
            )

    def _assert_has_operations(self) -> None:
        """
        Raise an error if the dataset does not have transforms applied
        """
        ops = None
        ops = self._api_operation_set.operations if self._api_operation_set else self._operations
        if not ops:
            raise errors.RasgoRuleViolation(
                "Dataset must have transforms applied in order to perform this action. "
                "Please apply transforms to your dataset to continue. "
            )

    def _get_or_create_op_set(self) -> OperationSet:
        """
        Get or create plus return the operation set for this dataset
        """
        # Online Dataset: Try to get existing OperationSet from the API first
        if not self._api_operation_set:
            self._refresh()

        # Offline Dataset: If there is no OpSet available in the API, create one
        if not self._api_operation_set:
            from pyrasgo.api.create import Create

            self._api_operation_set = Create()._operation_set(
                operations=self._operations,
                dataset_dependency_ids=self._dataset_dependencies,
                async_verbose=self._verbose,
            )

        return self._api_operation_set

    def _create_transform_function(self, transform: Transform) -> Callable:
        """
        Creates and returns a new function to dynamically attached to the Dataset obj on init

        New funcs docstring, name, and signature (params shown when inspecting/doing . tab on func)
        as well to improve notebook experience of using transforms for users

        Args:
            ds_transform_func: Function pointer of Dataset.transform()
            transform: Transform to read metadata and create new function for
        """

        # Create new function with 'transform_name` param set to this transform's name
        def f(*args, **kwargs) -> Dataset:
            return self.transform(transform_name=transform.name, *args, **kwargs)

        # Update func meta data for better inspection in notebook
        f.__name__ = transform.name
        f.__signature__ = _gen_func_signature(f, transform)
        f.__doc__ = _gen_func_docstring(transform)
        return f

    def _get_op_deps_parents_and_args(
        self,
        arguments: Dict[str, Union[str, int, List, Dict, Dataset]],
    ) -> Tuple[List[str], List[int], List[OperationCreate], Dict[str, Union[str, int, List, Dict, Dataset]]]:
        """
        Based on the input arguments a user supplied for this transform,
        determine and return a many things needed to initialize the next
        offline dataset. This includes
          - Operation Dependencies as list of FQTNs
          - Dataset Dependencies as list of unique dataset ids
          - List of parent operations for the next offline dataset
          - Updated args dict with Dataset objs converted to FQTN stings

        Args:
            arguments: The arguments a user supplied to the transform. This includes
                       'source_table' value we auto-populate

        Returns:
            Tuple of things needed to create next offline dataset
        """
        # Make copy of supplied transform arguments
        # since modifying in function
        arguments = arguments.copy()

        # Init lists to keep track of this operation's deps,
        # parent operations along with op set dependencies
        op_deps = []
        parent_ops = []
        ds_deps = self._dataset_dependencies.copy()

        # Always handle the `source_table` first to keep proper
        # order of parent operations
        source_table: Dataset = arguments.pop(SOURCE_TABLE_ARG_NAME)
        op_deps, parent_ops, ds_deps = self._update_op_deps__ds_deps__and_parent_ops(
            ds_arg=source_table, op_deps=op_deps, parent_ops=parent_ops, ds_deps=ds_deps
        )
        arguments[SOURCE_TABLE_ARG_NAME] = source_table.sql_alias

        arguments, new_op_deps, new_parent_ops, new_ds_deps = self._replace_ds_args(arguments)
        op_deps += new_op_deps
        parent_ops += new_parent_ops
        ds_deps += new_ds_deps
        # Return op deps, ds deps, parent ops, and updated arguments
        unique_parent_ops = []
        for op in parent_ops:
            if op not in unique_parent_ops:
                unique_parent_ops.append(op)
        return list(set(op_deps)), list(set(ds_deps)), unique_parent_ops, arguments

    @staticmethod
    def _replace_ds_args(arguments):
        """
        Traverses all args recursively and replaces instances of Datasets with fqtns and adds returns their dependencies
        """

        def replace_string(s):
            op_deps = []
            parent_ops = []
            ds_deps = []
            if isinstance(s, Dataset):
                op_deps.append(s.sql_alias)
                if s._api_dataset:
                    ds_deps.append(s._api_dataset.id)
                else:
                    parent_ops = s._operations
                s = s.sql_alias
            return s, op_deps, parent_ops, ds_deps

        def replace_list(l):
            all_op_deps = []
            all_parent_ops = []
            all_ds_deps = []
            for i in range(len(l)):
                if isinstance(l[i], dict):
                    l[i], op_deps, parent_ops, ds_deps = replace_dict(l[i])
                    all_op_deps += op_deps
                    all_parent_ops += parent_ops
                    all_ds_deps += ds_deps
                elif isinstance(l[i], list):
                    l[i], op_deps, parent_ops, ds_deps = replace_list(l[i])
                    all_op_deps += op_deps
                    all_parent_ops += parent_ops
                    all_ds_deps += ds_deps
                else:
                    l[i], op_deps, parent_ops, ds_deps = replace_string(l[i])
                    all_op_deps += op_deps
                    all_parent_ops += parent_ops
                    all_ds_deps += ds_deps
            return l, all_op_deps, all_parent_ops, all_ds_deps

        def replace_dict(d):
            all_op_deps = []
            all_parent_ops = []
            all_ds_deps = []
            for k in d.keys():
                if isinstance(d[k], dict):
                    d[k], op_deps, parent_ops, ds_deps = replace_dict(d[k])
                    all_op_deps += op_deps
                    all_parent_ops += parent_ops
                    all_ds_deps += ds_deps
                if isinstance(d[k], list):
                    d[k], op_deps, parent_ops, ds_deps = replace_list(d[k])
                    all_op_deps += op_deps
                    all_parent_ops += parent_ops
                    all_ds_deps += ds_deps
                else:
                    d[k], op_deps, parent_ops, ds_deps = replace_string(d[k])
                    all_op_deps += op_deps
                    all_parent_ops += parent_ops
                    all_ds_deps += ds_deps
            return d, all_op_deps, all_parent_ops, all_ds_deps

        return replace_dict(arguments)

    @staticmethod
    def _update_op_deps__ds_deps__and_parent_ops(
        ds_arg: Dataset, op_deps: List[str], parent_ops: List[OperationCreate], ds_deps: List[int]
    ) -> Tuple[List[str], List[OperationCreate], List[int]]:
        """
        Return updated DS args, deps, and op deps if arg to transform is type Dataset
        """
        op_deps = op_deps.copy()
        parent_ops = parent_ops.copy()
        ds_deps = ds_deps.copy()

        # Add input DS as operation dependency
        op_deps.append(ds_arg.sql_alias)

        # If the dataset from the API, make sure is published. If so update dataset deps
        if ds_arg._api_dataset:
            ds_deps.append(ds_arg._api_dataset.id)
        # If it's an offline dataset, grab its operations to set
        # as parents to output DS operations.
        # We need to make sure we aren't adding the same operation twice as well
        else:
            for ds_op in ds_arg._operations:
                if ds_op not in parent_ops:
                    parent_ops.append(ds_op)

        return op_deps, parent_ops, ds_deps


def _assert_value_types_of_args(
    transform: Transform,
    supplied_args: List[Dict[str, Union[str, int, List, Dict, Dataset]]],
    base_dataset: Dataset,
) -> None:
    """
    Raise exception if any of the supplied arguments are are not a valid type

    We especially need this to make sure args which expect datasets
    are ds objs and not fqtns, so we can add dependencies properly

    Args:
        transform: Transform applying
        supplied_args: Arguments of the supplied transform
        base_dataset: The base dataset which we're transforming
                      this is needed we can do `isinstance(arg, dataset.__class__)`
    """
    for transform_arg in transform.arguments:
        # We don't want to assert transform arguments
        # that are optional but not supplied, so skip
        # if not in user supplied args dict
        if transform_arg.name in supplied_args:
            supplied_arg_val = supplied_args[transform_arg.name]

            # If argument expects type 'table'
            # raise error if not of type 'Dataset'
            if transform_arg.type == TABLE_ARG_TYPE:
                if not isinstance(supplied_arg_val, base_dataset.__class__):
                    raise errors.ParameterValueError(
                        message=f"The {transform.name}() transform's parameter "
                        f"{transform_arg.name!r} requires the value to be "
                        f"a single Dataset obj. Got {type(supplied_arg_val)} instead"
                    )

            # If argument expects type 'table_list'
            # raise error if not of type List['Dataset']
            elif transform_arg.type == TABLE_LIST_ARG_TYPE:
                if not isinstance(supplied_arg_val, list) or any(
                    [not isinstance(x, base_dataset.__class__) for x in supplied_arg_val]
                ):
                    raise errors.ParameterValueError(
                        message=f"The {transform.name}() transform's parameter "
                        f"{transform_arg.name!r} requires the value to "
                        "be a non-empty list of Dataset objs."
                    )


def _get_transforms() -> List[Transform]:
    """
    Get and set available transforms from the API to be used
    directly as functions of Dataset if not retrieved yet
    """
    # Get available transforms from the API to be used directly as functions of Dataset
    from pyrasgo.api import Get

    try:
        return Get().transforms()
    except Exception:
        print('Unable to fetch available transforms from Rasgo.  Will not be able to transform this Dataset')
        return []


def _gen_func_signature(func: Callable, transform: Transform) -> inspect.Signature:
    """
    Creates and returns a transform param signature.

    This is shown documentation for the parameters when hitting shift tab in a notebook
    """
    # Get current signature of function
    sig = inspect.signature(func)

    # Create Signature Params for Transform Args
    transform_params = []
    for t_arg in transform.arguments:
        p = Parameter(name=t_arg.name, kind=Parameter.KEYWORD_ONLY)
        transform_params.append(p)

    # Add `operation_name` param as last in signature with type annotation
    op_name_param = Parameter(
        name='operation_name',
        kind=Parameter.KEYWORD_ONLY,
        annotation=Optional[str],
        default=None,
    )
    transform_params.append(op_name_param)

    # Return new signature
    return sig.replace(parameters=transform_params)


def _gen_func_docstring(transform: Transform) -> str:
    """
    Generate and return a docstring for a transform func
    with transform description, args, and return specified.
    """
    # Have start of docstring be transform description
    docstring = f"\n{transform.description}"

    # Add transform args to func docstring
    docstring = f"{docstring}\n  Args:"
    for t_arg in transform.arguments:
        docstring = f"{docstring}\n    {t_arg.name}: {t_arg.description}"
    docstring = f"{docstring}\n    operation_name: Name to set for the operation"

    # Add return to docstring
    docstring = (
        f"{docstring}\n\n  Returns:\n    Returns an new dataset with the referenced "
        f"{transform.name!r} added to this dataset's definition"
    )
    return docstring


def _add_statements_to_sql(
    sql: str,
    filters: Optional[List[str]] = None,
    order_by: Optional[List[str]] = None,
    limit: Optional[int] = None,
):
    if filters:
        sql = f"{sql} WHERE {' AND '.join(filters)}"
    if order_by:
        sql = f"{sql} ORDER BY {', '.join(order_by)}"
    if isinstance(limit, int):
        sql = f"{sql} LIMIT {limit}"
    return sql
