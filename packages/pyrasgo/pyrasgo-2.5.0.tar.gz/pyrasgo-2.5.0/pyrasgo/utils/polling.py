import time
from typing import Optional

from pyrasgo import errors, schemas


def poll_operation_set_async_status(
    task_request: schemas.OperationSetAsyncTask,
    delay_start=1,
    delay_max=1.5,
    backoff_multiplier=1.5,
    verbose=False,
) -> int:
    """
    Given some task request, this function will poll the API until the task hits a terminal status.

    If operation set created successfully with no errors, return operation set id
    """
    from pyrasgo.api import Get

    get = Get()

    operations_expected = len(task_request.request.operations)
    operations_created = 0
    delay = delay_start
    while True:
        time.sleep(delay)
        task_request = get._operation_set_async_status(task_request.id)

        # Get the status of the last event
        last_event_status = task_request.events[-1].event_type

        # Let the user know if this started
        if last_event_status == 'STARTED':
            if verbose:
                print(f'Operation set task {task_request.id} has started')

        # Is this progress? Keep track.
        if last_event_status == 'PROGRESSED':
            operations_created = task_request.events[-1].message['complete']
            if verbose:
                print(f'Operation set creation: {operations_created} of {operations_expected} operations complete')

        # Is this a failure? Throw an exception
        if last_event_status == 'FAILED':
            raise errors.APIError(
                f'Operation set creation failure: {task_request.events[-1].message}; '
                f'Progress: {operations_created} / {operations_expected}'
            )

        # Is this a success? Get out of this loop
        if last_event_status == 'FINISHED':
            operation_set_id = task_request.events[-1].message['operation_set_id']
            return operation_set_id

        # Still waiting? Grab a Snickers
        if delay < delay_max:
            delay = min(delay * backoff_multiplier, delay_max)
        if verbose:
            print('Poll waiting...')


def poll_dataset_publish(
    connection_obj,
    max_poll_attempts: int,
    status_tracking_obj: schemas.StatusTracking,
    poll_retry_rate: int,
    timeout: Optional[int] = None,
) -> schemas.Dataset:
    """
    When publishing a dataset async, this function tracks StatusTracking
    objects and returns a dataset, if one is successfully created

    Args:
        connection_obj: API object for calls
        max_poll_attempts: The maxiumum number of poll attempts
        status_tracking_obj: A StatusTracking schema to use for the first iteration of calls
        timeout: Max timeout window after which to fail the dataset publishing
        poll_retry_rate: Number of seconds between which to make another status tracking check
    """
    for i in range(1, max_poll_attempts):
        status_tracking_obj = schemas.StatusTracking(
            **connection_obj._get(f"/status-tracking/{status_tracking_obj.tracking_uuid}", api_version=2).json()
        )
        if status_tracking_obj.status == "completed":
            # TODO:
            # This try-except is here because in the API, some status tracking
            # messages return the dataset ID, and some return the dataset
            # object. We've got parsing in the SDK for now, but it sure would
            # be nice to just make this uniform in the API
            try:
                ds_id = int(status_tracking_obj.message)
            except ValueError:
                if status_tracking_obj.message.count("(") != 1:
                    raise errors.APIError(
                        "Status tracking object malformed - expecting string representation of Dataset Class"
                    )
                ds_id = int(
                    status_tracking_obj.message[
                        status_tracking_obj.message.find("(") + 1 : status_tracking_obj.message.find(")")
                    ]
                )
            return schemas.Dataset(**connection_obj._get(f"/datasets/{ds_id}", api_version=2).json())
        if status_tracking_obj.status == "failed":
            raise errors.APIError(f"Could not publish dataset: {status_tracking_obj.message}")
        if timeout and (poll_retry_rate * i) > timeout:
            raise errors.APITimeoutWarning("Timeout reached waiting for dataset creation.")
        time.sleep(poll_retry_rate)
    raise errors.APIError(
        f"Never received confirmation dataset was published "
        f"after max wait of {(max_poll_attempts * poll_retry_rate) // 60} minutes."
    )
