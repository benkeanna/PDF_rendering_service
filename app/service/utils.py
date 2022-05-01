from config import Config


def get_file_extension(filename):
    return filename.rsplit('.', 1)[1].lower()


def is_allowed_document(filename):
    return '.' in filename and get_file_extension(filename) == Config.DOCUMENT_EXTENSION
