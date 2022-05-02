import os

from config import Config


STATUS_PROCESSING = 'processing'
STATUS_DONE = 'done'


def get_document_folder(document_id):
    """Returns folder name in format: 'path-to-data/data/<document_id>/upload'."""
    folder_path = os.path.join(Config.UPLOAD_FOLDER, str(document_id), Config.UPLOADED_FILE_FOLDER_NAME)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    return folder_path


def get_document_path(document_id):
    document_name = f'{document_id}.{Config.DOCUMENT_EXTENSION}'
    document_path = os.path.join(get_document_folder(document_id), document_name)
    return document_path


def is_allowed_document(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == Config.DOCUMENT_EXTENSION
