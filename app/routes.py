from flask import request, abort

from app import app
from service.upload_document import upload_document, allowed_file


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/documents/', methods=['POST'])
def create_document():
    """uploads a file
        returns JSON { “id”: “<DOCUMENT_ID>? }"""
    if request.method == 'POST':
        if 'file' not in request.files:
            abort(400, 'File not found.')

        file = request.files['file']
        if file and allowed_file(file.filename):
            upload_document(file)
            return "ok", 200  # RETURN DOCUMENT ID
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
