from backend_app.app import app
from db import create_tables


if __name__ == '__main__':
    create_tables()
    app.run(host='127.0.0.1', port=8000, debug=False)
