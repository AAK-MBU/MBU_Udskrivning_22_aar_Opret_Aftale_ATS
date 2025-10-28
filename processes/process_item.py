"""Module to handle item processing"""

import logging

from datetime import datetime


from mbu_dev_shared_components.solteqtand.application import SolteqTandApp
from mbu_dev_shared_components.solteqtand.application.exceptions import (
    NotMatchingError,
    PatientNotFoundError,
)
from mbu_rpa_core.exceptions import BusinessError

from processes.application_handler import get_app

logger = logging.getLogger(__name__)


def process_item(item_data: dict, item_reference: str):
    """Docstring"""

    solteq_app = get_app()

    logger.info("Before trying handle_patient()")

    # This try-except catches all errors, and adds patient to manual list
    try:
        handle_patient(item_reference, solteq_app)

    except Exception as e:
        logger.info(f"ramte en fejl: {e}")

    logger.info("after trying handle_patient()")


def handle_patient(item_reference: str, solteq_app: SolteqTandApp):
    """
    Function to process items in Ikke meddelte aftaler.
    Process changes status of appointments and sends out messages to patient.
    If any business error, queue element is added to a manual list in an SQL database.
    """

    logger.info("inside handle_patient()")

    # Find the patient
    SSN = item_reference

    booking_reminder_data = {
        "comboBoxBookingType": "Z - 22 år - Borger fyldt 22 år",
        "comboBoxDentist": "Z - 22 år",
        "comboBoxChair": "Z - 22 år",
        "dateTimePickerStartTime": "07:45",
        "textBoxDuration": "5",
        "comboBoxStatus": "22 år - Afventer faglig vurdering",
        "textBoxBookingText": "Patient skal udskrives i forbindelse med 22 års fødselsdag",
        "futureDate": datetime.now().strftime("%d-%m-%Y"),
        "futureDateTime": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
    }

    logger.info("Indtaster CPR og laver opslag")
    try:
        solteq_app.open_patient(ssn=SSN)

        logger.info("Patientjournalen blev åbnet")

    except TimeoutError as e:
        missing_contact_info = solteq_app.find_element_by_property(
            control=solteq_app.app_window,
            name="Manglende kontaktoplysninger"
        )

        if missing_contact_info:
            raise BusinessError("Intet telefonnummer knyttet til patienten.") from e

        else:
            raise e from e

    except (NotMatchingError, PatientNotFoundError, Exception) as e:
        logger.error(str(e))

        raise BusinessError("Fejl ved åbning af patient") from e

    solteq_app.open_tab(tab_name="Stamkort")

    solteq_app.create_booking_reminder(booking_reminder_data=booking_reminder_data)
