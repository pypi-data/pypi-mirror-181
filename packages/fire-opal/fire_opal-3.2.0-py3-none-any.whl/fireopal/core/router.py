# Copyright 2022 Q-CTRL. All rights reserved.
#
# Licensed under the Q-CTRL Terms of service (the "License"). Unauthorized
# copying or use of this file, via any medium, is strictly prohibited.
# Proprietary and confidential. You may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#    https://q-ctrl.com/terms
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS. See the
# License for the specific language.

import json
import time
from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    Any,
    Dict,
    Optional,
)

import gql
from qctrlclient import GraphQLClient

from .action_status import ActionStatus
from .registry import RemoteRegistry


class BaseRouter(ABC):
    """Routes a request to execute a workflow."""

    @abstractmethod
    def __call__(self, workflow: str, data: Optional[Dict[str, Any]] = None) -> Any:
        """Given a workflow name and the corresponding data (if any),
        executes the workflow and returns the raw result.

        Parameters
        ----------
        workflow : str
            Name of the workflow to be executed.
        data : Dict[str, Any], optional
            Any data required by the workflow for execution.
        """


class ApiRouter(BaseRouter):
    """Remotely executes the workflow using the `startCoreWorkflow`
    GraphQL mutation.

    Parameters
    ----------
    client : GraphQLClient
        The GraphQL client used to make the request to execute
        the workflow remotely.
    registry : Registry
        The registry that the workflows being executed are
        registered in.
    """

    _COMPLETED_STATES = (ActionStatus.SUCCESS.value, ActionStatus.FAILURE.value)

    def __init__(self, client: GraphQLClient, registry: RemoteRegistry):
        self._client = client
        self._registry = registry

    def __call__(self, workflow, data=None):

        query = gql.gql(
            """
            mutation ($input: StartCoreWorkflowInput!) {
                startCoreWorkflow(input: $input) {
                    action {
                        modelId
                        status
                        result
                        errors {
                            exception
                            traceback
                        }
                    }
                    errors {
                        message
                        fields
                    }
                }
            }
        """
        )

        input_ = {
            "registry": self._registry.value,
            "workflow": workflow,
            "data": json.dumps(data),
        }

        response = self._client.execute(query, {"input": input_})

        # pylint:disable=unsubscriptable-object

        action_id = response["startCoreWorkflow"]["action"]["modelId"]
        status = response["startCoreWorkflow"]["action"]["status"]
        result = response["startCoreWorkflow"]["action"]["result"]
        errors = response["startCoreWorkflow"]["action"]["errors"]

        result = self.poll_for_completion(action_id, status, result, errors)
        return result

    def poll_for_completion(
        self, action_id: str, status: str, result: Any, errors: Any
    ) -> Any:
        """Polls the API waiting for the action to be completed.
        When completed, the `result` is returned.
        """

        _query = gql.gql(
            """
            query($modelId: String!) {
                action(modelId: $modelId) {
                    action {
                        status
                        errors {
                            exception
                            traceback
                        }
                        result
                    }
                    errors {
                        message
                    }
                }
            }
        """
        )

        while status not in self._COMPLETED_STATES:
            time.sleep(2)  # FIXME use progressive polling
            response = self._client.execute(_query, {"modelId": action_id})
            status = response["action"]["action"]["status"]
            result = response["action"]["action"]["result"]
            errors = response["action"]["action"]["errors"]

        if status == ActionStatus.FAILURE.value:
            raise RuntimeError(errors)

        if result is not None:
            result = json.loads(result)

        return result


class LocalRouter(BaseRouter):
    """Executes workflows using a resolver provided by a local
    package which implements the workflows.

    Parameters
    ----------
    resolver : BaseResolver
        A resolver object for the registry which contains all
        required workflows.
    """

    def __init__(self, resolver: "BaseResolver"):
        self._resolver = resolver

    def __call__(self, workflow, data=None):
        data = data or {}
        task = self._resolver.get_workflow_task_from_signature(workflow, **data)
        func = self._resolver(task)
        result = func()
        return result
