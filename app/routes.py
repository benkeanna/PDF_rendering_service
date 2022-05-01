from flask import request, abort, jsonify, send_file

from app import app
from worker import upload_document
from service.utils import is_allowed_document
from db.queries import read_document, read_page


@app.route('/')
def hello_world():
    """Dummy endpoint to check that the app is working."""
    return 'Welcome in PDF Rendering Service!'


@app.route('/documents/', methods=['POST'])
def create_document():
    """Returns document_id and initiates document processing."""
    if request.method == 'POST':
        if 'file' not in request.files:
            abort(400, 'No file posted.')

        file = request.files['file']
        if file and is_allowed_document(file.filename):
            document_id = upload_document(file)
            response = {'id': document_id}
            return response, 200
    else:
        abort(405)


@app.route('/documents/<document_id>/', methods=['GET'])
def get_document(document_id):
    """Returns document info."""
    if request.method == 'GET':
        document = read_document(document_id)
        if not document:
            abort(404, 'Document not found.')
        response = {'status': document['status'], 'n_pages': document['num_of_pages']}
        return response, 200

    else:
        abort(405)


@app.route('/documents/<document_id>/pages/<page_number>', methods=['GET'])
def get_document_pages(document_id, page_number):
    """Returns rendered document pages in PNG format."""
    if request.method == 'GET':
        pages = read_page(document_id, page_number)
        if not pages:
            abort(404, 'Page not found.')
        return send_file(pages['filepath'], mimetype='image/png')

    else:
        abort(405)
