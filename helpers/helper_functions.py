"""Helper functions"""

import sys
import os
import logging
import requests

from automation_server_client import AutomationServer
from automation_server_client._models import Workqueue

logger = logging.getLogger(__name__)


def fetch_next_workqueue(faglig_vurdering: bool = False):
    """
    Helper function to fetch the next workqueue in the overall process flow
    """

    next_workqueue_name = ""

    if "--borger_fyldt_22" in sys.argv:
        if faglig_vurdering:
            next_workqueue_name = "faglig_vurdering_udfoert"

        else:
            next_workqueue_name = "aftale_oprettet_i_solteq"

    elif "--aftale_oprettet_i_solteq" in sys.argv:
        next_workqueue_name = "formular_indsendt"

    elif "--formular_indsendt" in sys.argv:
        next_workqueue_name = "tandklinik_registreret_i_solteq"

    else:
        print("ERROR: NO VALID SYS ARGUMENT GIVEN!")
        sys.exit()

    ats_url = os.getenv("ATS_URL")
    ats_token = os.getenv("ATS_TOKEN")

    headers = {"Authorization": f"Bearer {ats_token}"}

    full_url = f"{ats_url}/workqueues/by_name/tan.udskrivning22.{next_workqueue_name}"

    response_json = requests.get(full_url, headers=headers, timeout=60).json()
    aftale_oprettet_queue_id = response_json.get("id")

    os.environ["ATS_WORKQUEUE_OVERRIDE"] = str(aftale_oprettet_queue_id)  # override it
    ats = AutomationServer.from_environment()
    workqueue = ats.workqueue()

    return workqueue


def fetch_workqueue_workitems(workqueue: Workqueue):
    """
    Helper function to fetch workitems for a given workqueue
    """

    ats_url = os.getenv("ATS_URL")
    ats_token = os.getenv("ATS_TOKEN")

    ats_headers = {"Authorization": f"Bearer {ats_token}"}

    full_url = f"{ats_url}/workqueues/{workqueue.id}/items"

    response_json = requests.get(full_url, headers=ats_headers, timeout=60).json()

    work_items = response_json.get("items")

    return work_items
