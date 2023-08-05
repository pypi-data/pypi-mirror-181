"""get_clusters SDK for MAPI"""
from __future__ import annotations

from concurrent.futures import Future
from typing import List, Optional, Union, overload

from typing_extensions import Literal

from mcli.api.engine.engine import run_plural_mapi_request
from mcli.api.model.cluster_details import ClusterDetails
from mcli.api.schema.query import named_query
from mcli.api.types import GraphQLQueryVariable, GraphQLVariableType
from mcli.models.mcli_cluster import Cluster

__all__ = ['get_clusters']


def get_cluster_schema(include_utilization) -> str:
    base = """
    name
    """

    if not include_utilization:
        return base + """
        allowedInstances {
            gpuType
            gpuNums
        }"""

    return base + """
    utilization {
        clusterInstanceUtils {
            clusterId
            gpuType
            gpusPerNode
            numNodes
            gpusUsed
            gpusAvailable
            gpusTotal
        }
        activeByUser {
            id
            createdAt
            userName
            runName
            gpuNum
        }
        queuedByUser {
            id
            createdAt
            userName
            runName
            gpuNum
        }
        anonymizeUsers
    }
    """


@overload
def get_clusters(
    clusters: Optional[Union[List[str], List[Cluster]]] = None,
    include_utilization: bool = False,
    timeout: Optional[float] = 10,
    future: Literal[False] = False,
) -> List[ClusterDetails]:
    ...


@overload
def get_clusters(
    clusters: Optional[Union[List[str], List[Cluster]]] = None,
    include_utilization: bool = False,
    timeout: Optional[float] = None,
    future: Literal[True] = True,
) -> Future[List[ClusterDetails]]:
    ...


def get_clusters(
    clusters: Optional[Union[List[str], List[Cluster]]] = None,
    include_utilization: bool = False,
    timeout: Optional[float] = 10,
    future: bool = False,
):
    """Get clusters available in the MosaicML Cloud

    Arguments:
        clusters (:class:`~mcli.models.mcli_cluster.Cluster`): List of
            :class:`~mcli.models.mcli_cluster.Cluster` objects or cluster name
            strings to get.
        include_utilization (``bool``): Include information on how the cluster is currently
            being utilized
        timeout (``Optional[float]``): Time, in seconds, in which the call should complete.
            If the run creation takes too long, a :exc:`~concurrent.futures.TimeoutError`
            will be raised. If ``future`` is ``True``, this value will be ignored.
        future (``bool``): Return the output as a :class:`~concurrent.futures.Future`. If True, the
            call to :func:`get_clusters` will return immediately and the request will be
            processed in the background. This takes precedence over the ``timeout``
            argument. To get the :class:`~mcli.models.cluster_details.ClusterDetails` output, use
            ``return_value.result()`` with an optional ``timeout`` argument.

    Raises:
        ``MAPIException``: If connecting to MAPI, raised when a MAPI communication error occurs
    """
    filters = {}
    if clusters:
        cluster_names = [c.name if isinstance(c, Cluster) else c for c in clusters]
        filters['name'] = {'in': cluster_names}

    query_function = 'getClusters'
    variable_data_name = 'getClustersData'
    variables = {
        variable_data_name: {
            'filters': filters
        },
    }

    graphql_variable: GraphQLQueryVariable = GraphQLQueryVariable(
        variableName=variable_data_name,
        variableDataName=variable_data_name,
        variableType=GraphQLVariableType.GET_CLUSTERS_INPUT,
    )

    query = named_query(
        query_name='GetClusters',
        query_function=query_function,
        query_items=get_cluster_schema(include_utilization),
        variables=[graphql_variable],
        is_mutation=False,
    )

    response = run_plural_mapi_request(
        query=query,
        query_function=query_function,
        return_model_type=ClusterDetails,
        variables=variables,
    )

    if not future:
        return response.result(timeout=timeout)
    else:
        return response
