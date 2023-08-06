"""Generic methods for endpoints
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from logging import getLogger
from typing import (
    TYPE_CHECKING,
    Any,
    ClassVar,
    Generic,
    Literal,
    Optional,
    TypeVar,
    cast,
)

from metabase_tools.exceptions import MetabaseApiException
from metabase_tools.models.generic_model import Item, MissingParam
from metabase_tools.utils.logging_utils import log_call

if TYPE_CHECKING:
    from metabase_tools import MetabaseApi

T = TypeVar("T", bound=Item)

logger = getLogger(__name__)


class Endpoint(ABC, Generic[T]):
    """Abstract base class for endpoints"""

    _BASE_EP: ClassVar[str]
    _STD_OBJ: ClassVar[type]
    _required_params: ClassVar[list[str]]
    _adapter: MetabaseApi

    def __init__(self, adapter: MetabaseApi):
        self._adapter = adapter

    @log_call
    def _request_list(
        self,
        http_verb: Literal["GET", "POST", "PUT", "DELETE"],
        endpoint: str,
        source: list[int],
    ) -> list[dict[str, Any]]:
        """Sends requests to API based on a list of objects

        Args:
            http_method (str): GET or POST or PUT or DELETE
            endpoint (str): Endpoint to use for request
            source (list[int] | list[dict]): List of targets or payloads

        Raises:
            InvalidParameters: Item in source is not an int or dict
            EmptyDataReceived: No data returned

        Returns:
            list[dict]: Aggregated results of all API calls
        """
        results = []

        for item in source:
            if isinstance(item, int):
                result = self._adapter.generic_request(
                    http_verb=http_verb, endpoint=endpoint.format(id=item)
                )
            else:
                raise TypeError(f"Expected list[int] but found {type(item)} in list")
            if isinstance(result, dict):
                results.append(result)
            if isinstance(result, list) and all(
                isinstance(item, dict) for item in result
            ):
                results.extend(result)
        if len(results) > 0:
            return results
        raise TypeError("Received empty list")

    @abstractmethod
    def get(self, targets: Optional[list[int]] = None) -> list[T]:
        """Generic method for returning an object or list of objects

        Args:
            targets (list[int], optional): IDs of the objects being requested

        Raises:
            InvalidParameters: Targets are not None or list[int]
            EmptyDataReceived: No data is received from the API

        Returns:
            list[T]: List of objects of the relevant type
        """
        if isinstance(targets, list) and all(isinstance(t, int) for t in targets):
            results = self._request_list(
                http_verb="GET",
                endpoint=self._BASE_EP + "/{id}",
                source=targets,
            )
            objs = [self._STD_OBJ(**result) for result in results]
            for obj in objs:
                obj.set_adapter(self._adapter)
            return objs

        if targets is None:
            # If no targets are provided, all objects of that type should be returned
            result = self._adapter.get(endpoint=self._BASE_EP)
            if isinstance(result, list):  # Validate data was returned
                # Unpack data into instances of the class and return
                objs = [
                    self._STD_OBJ(**record)
                    for record in result
                    if isinstance(record, dict)
                ]
                for obj in objs:
                    obj.set_adapter(self._adapter)
                return objs
        else:
            # If something other than None, list[int], raise error
            raise TypeError(f"Expected list[int] or None but received {type(targets)}")
        # If response.data was empty, raise error
        raise TypeError("Received empty list")

    @abstractmethod
    def _make_create(self, **kwargs: Any) -> T:
        """Generic method for creating an object

        Raises:
            InvalidParameters: Targets and jsons are both None

        Returns:
            T: Object of the relevant type
        """
        # Validate all required parameters were provided
        try:
            missing_params = [
                param
                for param in self._required_params
                if isinstance(kwargs[param], MissingParam)
            ]
            if len(missing_params) > 0:
                raise MetabaseApiException(
                    f"Missing required parameters: {''.join(missing_params)}"
                )
        except KeyError as error:
            raise MetabaseApiException from error

        # Eliminate parameters that were not provided
        details = {k: v for k, v in kwargs.items() if not isinstance(v, MissingParam)}

        result = self._adapter.post(endpoint=self._BASE_EP, json=details)
        if isinstance(result, dict):
            obj = self._STD_OBJ(**result)
            obj.set_adapter(adapter=self._adapter)
            return cast(T, obj)
        raise TypeError(f"Expected dict but received {type(result)}")

    @abstractmethod
    def search(
        self,
        search_params: list[dict[str, Any]],
        search_list: Optional[list[T]] = None,
    ) -> list[T]:
        """Method to search a list of objects meeting a list of parameters

        Args:
            search_params (list[dict]): Each dict contains search criteria and returns\
                 1 result
            search_list (list[T], optional): Provide to search against an existing \
                list, by default pulls from API

        Returns:
            list[T]: List of objects of the relevant type
        """
        objs = search_list or self.get()
        results = []
        for param in search_params:
            for obj in objs:
                obj_dict = obj.dict()
                for key, value in param.items():
                    if key in obj_dict and value == obj_dict[key]:
                        results.append(obj)
        return results
