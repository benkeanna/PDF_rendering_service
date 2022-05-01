import os
from uuid import uuid4

import worker
from config import Config
from db import queries
from service.utils import get_file_extension


def uploaded_document_folder(document_id):
    """Returns folder name in format: path-to-data/data/<document_id>/upload."""
    folder_path = os.path.join(Config.UPLOAD_FOLDER, str(document_id), Config.UPLOADED_FILE_FOLDER_NAME)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    return folder_path


def upload_document(file):
    # Save file to appropriate path.
    document_id = uuid4()
    filename = f'{uuid4().hex}.{get_file_extension(file.filename)}'
    filepath = os.path.join(uploaded_document_folder(document_id), filename)
    file.save(filepath)

    # Save document info to DB.
    queries.create_document(document_id=document_id, filepath=filepath)

    # Queue parsing PDF to PNG
    worker.parse_pdf(filepath, document_id)

    return document_id
