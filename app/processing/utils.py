from config import Config


def is_allowed_document(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == Config.DOCUMENT_EXTENSION
