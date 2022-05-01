import os

from config import Config


def pages_folder(document_id):
    folder_path = os.path.join(Config.UPLOAD_FOLDER, str(document_id), Config.PAGES_FOLDER_NAME)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    return folder_path
