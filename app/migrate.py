"""just a simple one-off script, I would use Alembic in the real world. """

if __name__ == '__main__':
    from app import db
    from db.models import Document, Page
    db.create_all()
