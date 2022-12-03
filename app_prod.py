from avionics_dash_server.common.constants import App
import os

if __name__ == "__main__":
    # Third-Party Library
    from dotenv import load_dotenv

    # Load Environment Variables
    load_dotenv()

    if os.environ["APP_ENV"] == App.PROD_ENV:
        # Custom Library
        from avionics_dash_server.app import create_app

        app = create_app()
