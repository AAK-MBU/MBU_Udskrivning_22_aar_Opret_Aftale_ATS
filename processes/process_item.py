"""
Handles patient processing logic for the 'Udskrivning 22 år' workflow.

This module is responsible for interacting with Solteq Tand via the
`mbu_dev_shared_components.solteqtand` library to locate patient records
and create appropriate booking reminders for patients turning 22 years old.

The processing functions handle potential business exceptions, logging, and
fallbacks to manual handling if automation cannot complete successfully.
"""

import logging

from datetime import datetime

from mbu_solteqtand_shared_components.application import SolteqTandApp
from mbu_solteqtand_shared_components.application.exceptions import (
    NotMatchingError,
    PatientNotFoundError,
)
from mbu_rpa_core.exceptions import BusinessError

from processes.application_handler import get_app

logger = logging.getLogger(__name__)


def process_item(item_data: dict, item_reference: str):
    """
    Processes a single workitem from the ATS queue.

    This function initializes the Solteq application session and attempts
    to process the provided patient reference. If any unexpected error
    occurs, the patient will be flagged for manual follow-up.

    Args:
        item_data (dict): Raw data payload from the ATS work item.
        item_reference (str): The reference identifier (typically CPR/SSN) of the patient to be processed.
    """

    logger.info(f"item_data: {item_data}")
    logger.info(f"item_reference: {item_reference}")

    solteq_app = get_app()

    logger.info("Before trying handle_patient()")

    # This try-except catches all errors, and adds patient to manual list
    try:
        handle_patient(item_reference=item_reference, solteq_app=solteq_app)

    except Exception as e:
        logger.info(f"ramte en fejl: {e}")

        raise

    logger.info("After trying handle_patient()")


def handle_patient(item_reference: str, solteq_app: SolteqTandApp):
    """
    Performs all patient-specific automation in Solteq Tand.

    This function:
      - Opens the patient journal using the given CPR number.
      - Navigates to the correct tab in Solteq Tand.
      - Creates a booking reminder for the '22 år - Afventer faglig vurdering' process.

    If any business error or patient-related issue is encountered,
    the case is raised as a `BusinessError`, so the calling function can
    handle manual follow-up.

    Args:
        item_reference (str): The patient's SSN number.
        solteq_app (SolteqTandApp): Active instance of the Solteq Tand application.

    Raises:
        BusinessError: If patient data is incomplete, missing, or cannot be processed.
    """

    logger.info("Inside handle_patient()")

    # Find the patient
    ssn = item_reference

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
        solteq_app.open_patient(ssn=ssn)

        logger.info("Patientjournalen blev åbnet")

    except TimeoutError as e:
        missing_contact_info = solteq_app.find_element_by_property(
            control=solteq_app.app_window,
            name="Manglende kontaktoplysninger"
        )

        if missing_contact_info:
            raise BusinessError("Intet telefonnummer knyttet til patienten.") from e

        raise e from e

    except (NotMatchingError, PatientNotFoundError, Exception) as e:
        logger.error(str(e))

        raise BusinessError("Fejl ved åbning af patient") from e

    logger.info("Åbner 'Stamkort'")
    solteq_app.open_tab(tab_name="Stamkort")

    logger.info("Opretter aftale")
    solteq_app.create_booking_reminder(booking_reminder_data=booking_reminder_data, booking_clinic="Tandplejen Aarhus")
