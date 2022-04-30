import os
from uuid import uuid4


from config import Config
from db import queries


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS


def upload_document(file):
    document_id = uuid4()
    filename = uuid4().hex + '.pdf'  # TODO PDF PDF PDF
    filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
    file.save(filepath)
    queries.create_document(document_id=document_id, filepath=filepath)
    return document_id
