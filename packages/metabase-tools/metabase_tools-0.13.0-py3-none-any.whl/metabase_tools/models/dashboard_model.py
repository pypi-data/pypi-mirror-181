"""Classes related to dashboard endpoints
"""
from __future__ import annotations

from datetime import datetime
from logging import getLogger
from typing import TYPE_CHECKING, Any, ClassVar, Optional

from pydantic import Field, PrivateAttr

from metabase_tools.models.generic_model import Item, MissingParam
from metabase_tools.models.user_model import UserItem
from metabase_tools.utils.logging_utils import log_call

if TYPE_CHECKING:
    from metabase_tools.metabase import MetabaseApi

logger = getLogger(__name__)


class DashboardItem(Item):
    """Dashboard object class with related methods"""

    _BASE_EP: ClassVar[str] = "/dashboard/{id}"

    _adapter: Optional[MetabaseApi] = PrivateAttr(None)

    description: Optional[str]
    archived: bool
    collection_position: Optional[int]
    creator: Optional[UserItem]
    enable_embedding: bool
    collection_id: Optional[int]
    show_in_getting_started: bool
    name: str
    caveats: Optional[str]
    creator_id: int
    updated_at: datetime
    made_public_by_id: Optional[int]
    embedding_params: Optional[dict[str, Any]]
    id: int
    position: Optional[int]
    parameters: list[dict[str, Any]]
    favorite: Optional[bool]
    created_at: datetime
    public_uuid: Optional[str]
    points_of_interest: Optional[str]
    can_write: Optional[bool]
    ordered_cards: Optional[list[dict[str, Any]]]
    param_fields: Optional[dict[str, Any]]
    param_values: Optional[dict[str, Any]]
    cache_ttl: Optional[int]
    entity_id: Optional[str]
    last_edit_info: Optional[dict[str, Any]] = Field(alias="last-edit-info")
    collection_authority_level: Optional[int]
    is_app_page: Optional[bool]

    @log_call
    def refresh(self: DashboardItem) -> DashboardItem:
        """Returns refreshed copy of the dashboard

        Returns:
            DashboardItem: self
        """
        return super().refresh()

    @log_call
    def delete(self: DashboardItem) -> None:
        """Deletes the dashboard"""
        return super().delete()

    def _make_update(self: DashboardItem, **kwargs: Any) -> DashboardItem:
        """Makes update request

        Args:
            self (DashboardItem)

        Returns:
            DashboardItem: self
        """
        return super()._make_update(**kwargs)

    @log_call
    def update(
        self: DashboardItem,
        parameters: Optional[list[dict[str, Any]] | MissingParam] = MissingParam(),
        points_of_interest: Optional[str | MissingParam] = MissingParam(),
        description: Optional[str | MissingParam] = MissingParam(),
        archived: Optional[bool | MissingParam] = MissingParam(),
        collection_position: Optional[int | MissingParam] = MissingParam(),
        show_in_getting_started: Optional[bool | MissingParam] = MissingParam(),
        enabled_embedding: Optional[bool | MissingParam] = MissingParam(),
        collection_id: Optional[int | MissingParam] = MissingParam(),
        name: Optional[str | MissingParam] = MissingParam(),
        caveats: Optional[str | MissingParam] = MissingParam(),
        embedding_params: Optional[dict[str, Any] | MissingParam] = MissingParam(),
        position: Optional[int | MissingParam] = MissingParam(),
        **kwargs: Any,
    ) -> DashboardItem:
        """Updates an existing dashboard item

        Args:
            self (DashboardItem)
            parameters (list[dict[str, Any]], optional)
            points_of_interest (str, optional)
            description (str, optional)
            archived (bool, optional)
            collection_position (int, optional)
            show_in_getting_started (bool, optional)
            enabled_embedding (bool, optional)
            collection_id (int, optional)
            name (str, optional)
            caveats (str, optional)
            embedding_params (dict[str, Any], optional)
            position (int, optional)

        Returns:
            DashboardItem: _description_
        """
        return self._make_update(
            parameters=parameters,
            points_of_interest=points_of_interest,
            description=description,
            archived=archived,
            collection_position=collection_position,
            show_in_getting_started=show_in_getting_started,
            enabled_embedding=enabled_embedding,
            collection_id=collection_id,
            name=name,
            caveats=caveats,
            embedding_params=embedding_params,
            position=position,
            **kwargs,
        )
