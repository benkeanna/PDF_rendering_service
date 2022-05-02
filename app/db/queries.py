from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from utils.document import STATUS_PROCESSING, STATUS_DONE
from config import Config
from db.models import Document, Page

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(engine)


def read_document(document_id):
    with Session.begin() as session:
        document = session.query(Document).filter_by(id=str(document_id)).first()
        if not document:
            return None
        return document.as_dict


def create_document(document_id, filepath):
    document = Document(id=document_id, status=STATUS_PROCESSING, filepath=filepath)
    with Session.begin() as session:
        session.add(document)
        session.commit()


def update_document(document_id, num_of_pages):
    with Session.begin() as session:
        document = session.query(Document).filter_by(id=str(document_id)).first()
        document.status = STATUS_DONE
        document.num_of_pages = num_of_pages
        document.modified_at = datetime.utcnow()
        session.commit()


def create_page(document_id, filepath, page_number):
    page = Page(document_id=document_id, filepath=filepath, page_number=page_number)
    with Session.begin() as session:
        session.add(page)
        session.commit()


def read_page(document_id, page_number):
    with Session.begin() as session:
        page = session.query(Page).filter_by(document_id=document_id, page_number=page_number).first()
        if not page:
            return None
        return page.as_dict
