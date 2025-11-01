from api_gateway import create_gateway_app

api_gateway_app = create_gateway_app()

if __name__ == "__main__":
    api_gateway_app.run(port=5005)