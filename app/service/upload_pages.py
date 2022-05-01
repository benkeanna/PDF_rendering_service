import os

from pdf2image import convert_from_path

from config import Config
from db.queries import create_page, update_document


def pages_folder(document_id):
    """Returns folder name in format: path-to-data/data/<document_id>/pages."""
    folder_path = os.path.join(Config.UPLOAD_FOLDER, str(document_id), Config.PAGES_FOLDER_NAME)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    return folder_path


def upload_pages(document_id, filepath):
    images = convert_from_path(filepath)

    for page_number in range(len(images)):
        filename = f'page{str(page_number)}.{Config.PAGE_EXTENSION}'
        filepath = os.path.join(pages_folder(document_id), filename)
        images[page_number].save(filepath, 'PNG')

        create_page(document_id, filepath, page_number)

    # Update document status and number of pages.
    update_document(document_id=document_id, num_of_pages=len(images))
