from flask import Flask, request, abort, jsonify

from worker import parse_pdf

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/documents/', methods=['GET'])  # TODO POST
def create_document():
    """uploads a file
        returns JSON { “id”: “<DOCUMENT_ID>? }"""

    if request.method == 'GET':
        return jsonify(parse_pdf.send()), 200

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
