"""Helper functions"""

import logging

from automation_server_client import WorkItem

logger = logging.getLogger(__name__)


def get_item_info(item: WorkItem):
    """Unpack item"""
    return item.data["item"]["data"], item.data["item"]["reference"]


def init_logger():
    """Initialize the root logger with JSON formatting."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(module)s.%(funcName)s:%(lineno)d — %(message)s",
        datefmt="%H:%M:%S",
    )
