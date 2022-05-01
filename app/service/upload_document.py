import os

from config import Config


def uploaded_document_folder(document_id):
    """Returns folder name in format: 'path-to-data/data/<document_id>/upload'."""
    folder_path = os.path.join(Config.UPLOAD_FOLDER, str(document_id), Config.UPLOADED_FILE_FOLDER_NAME)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    return folder_path


def get_document_path(document_id):
    filename = f'{document_id}.{Config.DOCUMENT_EXTENSION}'
    filepath = os.path.join(uploaded_document_folder(document_id), filename)
    return filepath
