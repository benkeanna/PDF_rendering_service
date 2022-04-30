from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('config.Config')
db = SQLAlchemy(app)


if __name__ == '__main__':
    """Using DEV setup.
    I would use Nginx and Gunicorn for production setup and follow this https://testdriven.io/blog/dockerizing-flask-with-postgres-gunicorn-and-nginx/?fbclid=IwAR38OY8HqFiu_wsTk7vfTsLfTaK7dUk4pxfGhQiRr82nqq1CSP6nPzEp48w.
    """
    from routes import *
    app.run(debug=True, host='0.0.0.0', port=8000)
