# Standard Library
import logging

# Custom Library
from avionics_dash_server.app import app

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Initializing Avionics-Dash!")
    app.run()
