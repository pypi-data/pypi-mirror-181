"""Classes related to activity endpoints
"""
from __future__ import annotations

from datetime import datetime
from logging import getLogger
from typing import TYPE_CHECKING, Any, Optional

from metabase_tools.models.database_model import DatabaseItem
from metabase_tools.models.generic_model import Item
from metabase_tools.models.user_model import UserItem
from metabase_tools.utils.logging_utils import log_call

if TYPE_CHECKING:
    from metabase_tools.metabase import MetabaseApi

logger = getLogger(__name__)


class ActivityItem(Item):
    """Activity object class with related methods"""

    id: int
    table_id: Optional[int]
    table: Optional[str]
    database_id: Optional[int]
    model_exists: Optional[bool]
    topic: Optional[str]
    custom_id: Optional[int]
    details: Optional[dict[str, Any]]
    model_id: Optional[int]
    database: Optional[DatabaseItem]
    user_id: Optional[int]
    timestamp: datetime
    user: Optional[UserItem]
    model: Optional[str]

    @log_call
    def set_adapter(self, adapter: MetabaseApi) -> None:
        """Sets the adapter on an object

        Args:
            adapter (MetabaseApi): Connection to MetabaseApi
        """
        super().set_adapter(adapter=adapter)
