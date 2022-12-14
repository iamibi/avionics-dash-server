if __name__ == "__main__":
    # Third-Party Library
    from dotenv import load_dotenv

    # Load Environment Variables
    load_dotenv()

    # Custom Library
    from avionics_dash_server.app import create_app

    app = create_app()
    app.run(debug=True)
