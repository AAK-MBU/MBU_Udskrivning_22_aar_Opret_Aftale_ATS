"""Module for fetching citizen that have turned 22 as of today's date"""

import os

from mbu_dev_shared_components.solteqtand.database.db_handler import SolteqTandDatabase

SOLTEQ_TAND_DB_CONN_STRING = os.getenv("DBCONNECTIONSTRINGSOLTEQTAND")


# pylint: disable=unused-argument
def retrieve_citizens(prefix: str):
    """Main function to execute the script."""

    citizens_turned_22 = []
    data = []
    references = []

    db_handler = SolteqTandDatabase(conn_str=SOLTEQ_TAND_DB_CONN_STRING)

    citizen_in_age_range = get_citizen_turning_22_today(db_handler, prefix)

    for citizen_solteq in citizen_in_age_range:
        patient_id = citizen_solteq["patientId"]
        citizen_cpr = citizen_solteq["cpr"]
        citizen_full_name = f"{citizen_solteq['firstName']} {citizen_solteq['lastName']}"

        # Add to result list
        citizens_turned_22.append({
            "patientId": patient_id,
            "cpr": citizen_cpr,
            "fullName": citizen_full_name,
        })

    for citizen in citizens_turned_22:
        references.append(citizen_cpr)
        data.append(citizen)

    return data, references


def get_citizen_turning_22_today(db_handler: SolteqTandDatabase, prefix):
    """
    Get citizen who are exactly 22 years old based on CPR.
    """

    query = """
        SELECT
            patientId,
            firstName,
            lastName,
            cpr
        FROM
            [tmtdata_prod].[dbo].[PATIENT]
        WHERE
            cpr LIKE ?
        ORDER BY
            firstName, lastName;
    """

    like_param = f"{prefix}%"

    # pylint: disable=protected-access
    return db_handler._execute_query(query, params=(like_param,))
