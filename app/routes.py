from flask import request, abort, jsonify, send_file, make_response

from app import app
from worker import upload_document
from utils.document import is_allowed_document
from db.queries import read_document, read_page


@app.route('/documents/', methods=['POST'])
def create_document():
    """Returns document_id and initiates document processing."""
    if request.method == 'POST':
        if 'file' not in request.files:
            abort(400, description='No file posted.')

        file = request.files['file']
        if file and is_allowed_document(file.filename):
            document_id = upload_document(file)
            response = {'id': document_id}
            return response, 200
        else:
            abort(make_response(jsonify(message='File with this extension not allowed.'), 400))
    else:
        abort(make_response(jsonify('Method not allowed'), 405))


@app.route('/documents/<document_id>/', methods=['GET'])
def get_document(document_id):
    """Returns document info."""
    if request.method == 'GET':
        document = read_document(document_id)
        if not document:
            abort(make_response(jsonify(message='Document not found.'), 404))
        # Keeping the 'n_pages' because some service in the real world can already count on it,
        # but I would rename it if I knew I could.
        response = {'status': document['status'], 'n_pages': document['num_of_pages']}
        return response, 200

    else:
        abort(make_response(jsonify('Method not allowed'), 405))


@app.route('/documents/<document_id>/pages/<page_number>', methods=['GET'])
def get_document_pages(document_id, page_number):
    """Returns rendered document page in PNG format."""
    # Cache for the pages could be good.
    if request.method == 'GET':
        pages = read_page(document_id, page_number)
        if not pages:
            abort(make_response(jsonify(message='Page not found.'), 404))
        return send_file(pages['filepath'], mimetype='image/png')

    else:
        abort(make_response(jsonify('Method not allowed'), 405))
