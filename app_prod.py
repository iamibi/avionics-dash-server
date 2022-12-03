# Standard Library
import os
import logging

# Custom Library
from avionics_dash_server.common.constants import App

logger = logging.getLogger(__name__)


def prod_deploy():
    logger.info("Starting Prod Service!")

    # Third-Party Library
    from dotenv import load_dotenv

    # Load Environment Variables
    load_dotenv()

    # Custom Library
    from avionics_dash_server.app import create_app

    app = create_app()
    app.run(host="0.0.0.0", port=8000, debug=False)
