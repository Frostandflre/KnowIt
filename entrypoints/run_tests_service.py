from tests_service import create_tests_app

tests_app = create_tests_app()

if __name__ == "__main__":
    tests_app.run(port=5002)