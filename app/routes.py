from flask import request, abort, jsonify

from app import app
from service.upload_document import upload_document
from service.utils import allowed_document


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
        if file and allowed_document(file.filename):
            document_id = upload_document(file)
            response = {'id': document_id}
            return jsonify(response), 200
    else:
        abort(405)


@app.route('/documents/<document_id>/', methods=['GET'])
def get_document(document_id):
    """returns JSON """
    if request.method == 'GET':
        response = {'status': 'processing|done', 'n_pages': 1}
        return jsonify(response), 200

    else:
        abort(405)


@app.route('/documents/<document_id>/pages/', methods=['GET'])
def get_document_pages(document_id):
    """return rendered image png"""
    if request.method == 'GET':
        return document_id, 200

    else:
        abort(405)
