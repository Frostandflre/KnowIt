from main_service import create_main_app
import os

main_app = create_main_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    main_app.run(host="0.0.0.0", port=port, debug=False)