from flask import request, abort, jsonify

from app import app
from db.queries import read_document
from service.upload_document import upload_document
from service.utils import is_allowed_document


@app.route('/')
def hello_world():
    """Dummy endpoint to check that the app is working."""
    return 'Welcome in PDF Rendering Service!'


@app.route('/documents/', methods=['POST'])
def create_document():
    """Returns document_id and initiates document upload."""
    if request.method == 'POST':
        if 'file' not in request.files:
            abort(400, 'File not found.')

        file = request.files['file']
        if file and is_allowed_document(file.filename):
            document_id = upload_document(file)
            response = {'id': document_id}
            return jsonify(response), 200
    else:
        abort(405)


@app.route('/documents/<document_id>/', methods=['GET'])
def get_document(document_id):
    """Returns document info."""
    if request.method == 'GET':
        document = read_document(document_id)
        response = {'status': document['status'], 'n_pages': document['num_of_pages']}
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
