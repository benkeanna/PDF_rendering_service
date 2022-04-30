import os

from flask import request, jsonify, abort, Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

from config import allowed_file
from worker import parse_pdf

app = Flask(__name__)
app.config.from_object('config.Config')
db = SQLAlchemy(app)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/documents/', methods=['GET', 'POST'])  # TODO POST
def create_document():
    """uploads a file
        returns JSON { “id”: “<DOCUMENT_ID>? }"""

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return "no file", 400
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            return "no file name", 400
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return "ok", 200
    else:
        abort(405)


@app.route('/documents/<document_id>/', methods=['GET'])
def get_document(document_id):
    """returns JSON { “status”: “processing|done”, “n_pages”: NUMBER }"""
    if request.method == 'GET':
        return document_id, 200

    else:
        abort(405)


@app.route('/documents/<document_id>/pages/', methods=['GET'])
def get_document_page(document_id):
    """return rendered image png"""
    if request.method == 'GET':
        return document_id, 200

    else:
        abort(405)


if __name__ == '__main__':
    """Using DEV setup.
    I would use Nginx and Gunicorn for production setup and follow this https://testdriven.io/blog/dockerizing-flask-with-postgres-gunicorn-and-nginx/?fbclid=IwAR38OY8HqFiu_wsTk7vfTsLfTaK7dUk4pxfGhQiRr82nqq1CSP6nPzEp48w.
    """
    app.run(debug=True, host='0.0.0.0', port=8000)
