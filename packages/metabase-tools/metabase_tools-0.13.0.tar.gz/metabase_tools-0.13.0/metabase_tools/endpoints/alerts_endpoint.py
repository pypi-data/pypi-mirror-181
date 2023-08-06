"""Classes related to alert endpoints
"""

from __future__ import annotations

from logging import getLogger
from typing import Any, ClassVar, Optional

from packaging.version import Version

from metabase_tools.endpoints.generic_endpoint import Endpoint
from metabase_tools.models.alert_model import AlertItem
from metabase_tools.models.generic_model import MissingParam
from metabase_tools.utils.logging_utils import log_call

logger = getLogger(__name__)


class Alerts(Endpoint[AlertItem]):
    """Alert related endpoint methods"""

    _BASE_EP: ClassVar[str] = "/alert"
    _STD_OBJ: ClassVar[type] = AlertItem

    _required_params: ClassVar[list[str]] = [
        "alert_condition",
        "card",
        "channels",
        "alert_first_only",
        "alert_above_goal",
    ]

    @log_call
    def get(self, targets: Optional[list[int]] = None) -> list[AlertItem]:
        """Fetch list of alerts

        Args:
            targets (list[int], optional): If provided, the list of alerts to fetch

        Returns:
            list[AlertItem]
        """
        if targets and not isinstance(targets, list):
            raise TypeError
        if self._adapter and self._adapter.server_version >= Version("v0.41"):
            return super().get(targets=targets)  # standard if supported by version
        if targets and isinstance(targets, list):
            return [x for x in super().get() if x.id in targets]  # get all and filter
        return super().get()  # get all

    def get_by_card(self, targets: list[int]) -> list[AlertItem]:
        """Get all alerts for the given card IDs

        Args:
            targets (list[int]): List of card IDs

        Returns:
            list[AlertItem]: List of associated alerts
        """
        result = self._request_list(
            "GET", endpoint="/alert/question/{id}", source=targets
        )
        alerts = [AlertItem(**x) for x in result]
        for alert in alerts:
            alert.set_adapter(self._adapter)
        return alerts

    def _make_create(self, **kwargs: Any) -> AlertItem:
        """Makes create request

        Args:
            self (AlertItem)

        Returns:
            AlertItem: self
        """
        return super()._make_create(**kwargs)

    @log_call
    def create(
        self,
        visualization_settings: dict[str, Any] | MissingParam = MissingParam(),
        name: str | MissingParam = MissingParam(),
        dataset_query: dict[str, Any] | MissingParam = MissingParam(),
        display: str | MissingParam = MissingParam(),
        description: Optional[str | MissingParam] = MissingParam(),
        collection_position: Optional[int | MissingParam] = MissingParam(),
        result_metadata: Optional[list[dict[str, Any]] | MissingParam] = MissingParam(),
        metadata_checksum: Optional[str | MissingParam] = MissingParam(),
        collection_id: Optional[int | MissingParam] = MissingParam(),
        **kwargs: Any,
    ) -> AlertItem:
        """Creates a new alert

        Args:
            visualization_settings (dict[str, Any])
            name (str)
            dataset_query (dict[str, Any])
            display (str)
            description (str, optional)
            collection_position (int, optional)
            result_metadata (list[dict[str, Any]], optional)
            metadata_checksum (str, optional)
            collection_id (int, optional)

        Returns:
            AlertItem
        """
        return self._make_create(
            visualization_settings=visualization_settings,
            description=description,
            collection_position=collection_position,
            result_metadata=result_metadata,
            metadata_checksum=metadata_checksum,
            collection_id=collection_id,
            name=name,
            dataset_query=dataset_query,
            display=display,
            **kwargs,
        )

    @log_call
    def search(
        self,
        search_params: list[dict[str, Any]],
        search_list: Optional[list[AlertItem]] = None,
    ) -> list[AlertItem]:
        """Method to search a list of alerts meeting a list of parameters

        Args:
            search_params (list[dict]): Each dict contains search criteria and returns\
                 1 result
            search_list (list[AlertItem], optional): Provide to search an existing \
                list, by default pulls from API

        Returns:
            list[AlertItem]: List of alerts of the relevant type
        """
        return super().search(search_params=search_params, search_list=search_list)
