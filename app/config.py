import os

UPLOAD_FOLDER = os.path.abspath("../data")
ALLOWED_EXTENSIONS = {'pdf'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class Config:
    """Flask configuration."""

    # Credentials would not be saved in repo.
    # I would let SRE or Infra team handle this securely.
    SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@db:5432/pdf'
    SECRET_KEY = '2d3dd5803d5e2e6ef3f273a3b9390d1e29179e7b93ab506b130b816261ef493d'
    UPLOAD_FOLDER = UPLOAD_FOLDER
