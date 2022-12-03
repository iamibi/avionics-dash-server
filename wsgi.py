from avionics_dash_server.app import create_app
import logging
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Starting Prod Service!")

    # Third-Party Library
    from dotenv import load_dotenv

    # Load Environment Variables
    load_dotenv()

    app = create_app()
    app.run()
