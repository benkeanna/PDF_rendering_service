from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import Config
from db.models import Document, Page

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(engine)


def create_document(document_id, filepath):
    document = Document(document_id=document_id, status='processing', filepath=filepath)
    with Session.begin() as session:
        session.add(document)
        session.commit()
