"""
This is the main entry point for the process
"""

import logging

from mbu_dev_shared_components.solteqtand.application import SolteqTandApp
from mbu_dev_shared_components.database.connection import RPAConnection

from helpers import config

logger = logging.getLogger(__name__)


if __name__ == "__main__":

    with RPAConnection(db_env="PROD", commit=False) as rpa_conn:
        creds = rpa_conn.get_credential("solteq_tand_svcrpambu001")
        username = creds["username"]
        password = creds["decrypted_password"]

    solteq_app = SolteqTandApp(app_path=config.APP_PATH, username=username, password=password)

    solteq_app.start_application()

    solteq_app.login()

    solteq_app.open_patient(ssn="1110109996")
