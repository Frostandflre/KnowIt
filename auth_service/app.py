from auth_service import create_auth_app

auth_app = create_auth_app()

if __name__ == "__main__":
    auth_app.run(port=5001)