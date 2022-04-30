import os


class Config:
    """Flask configuration."""

    # Credentials would not be saved in repo.
    # Depending on deploy type I would use appropriate tools, e.g. vault, sops, docker secret etc.
    SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@db:5432/pdf'
    SECRET_KEY = '2d3dd5803d5e2e6ef3f273a3b9390d1e29179e7b93ab506b130b816261ef493d'
    UPLOAD_FOLDER = os.path.abspath("../data")
    ALLOWED_EXTENSIONS = {'pdf'}
