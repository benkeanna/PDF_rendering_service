from sqlalchemy import Column, Integer, String, ForeignKey
from app import db


class Document(db.Model):
    __tablename__ = 'document'
    id = Column(String(50), primary_key=True)
    status = Column(String(50))
    filepath = Column(String(255), unique=True)
    num_of_pages = Column(Integer, unique=True)

    def __init__(self, status=None, filepath=None, num_of_pages=None):
        self.status = status
        self.filepath = filepath
        self.num_of_pages = num_of_pages

    def __repr__(self):
        return f'<Document {self.id!r}>'


class Page(db.Model):
    __tablename__ = 'document_page'
    id = Column(Integer, primary_key=True)
    document_id = Column(String(50), ForeignKey("document.id"), nullable=False)
    filepath = Column(String(255), unique=True)
    page_number = Column(Integer, unique=True)

    def __init__(self, status=None, num_of_pages=None):
        self.status = status
        self.num_of_pages = num_of_pages

    def __repr__(self):
        return f'<Page {self.id!r}>'
