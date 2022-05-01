from config import Config


def document_extension(filename):
    return filename.rsplit('.', 1)[1].lower()


def allowed_document(filename):
    return '.' in filename and document_extension(filename) in Config.ALLOWED_EXTENSIONS
