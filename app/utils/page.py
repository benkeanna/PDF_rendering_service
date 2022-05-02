import os

from PIL import Image, ImageOps

from config import Config


def get_pages_folder(document_id):
    """Returns folder name in format: 'path-to-data/data/<document_id>/pages'."""
    page_path = os.path.join(Config.UPLOAD_FOLDER, str(document_id), Config.PAGES_FOLDER_NAME)
    if not os.path.exists(page_path):
        os.makedirs(page_path)
    return page_path


def get_page_path(document_id, page_number):
    page_name = f'page{str(page_number)}.{Config.PAGE_EXTENSION}'
    page_path = os.path.join(get_pages_folder(document_id), page_name)
    return page_path


def resize_page_if_needed(filepath):
    with Image.open(filepath) as image:
        resized_image = ImageOps.contain(image, (Config.MAX_PAGE_WIDTH, Config.MAX_PAGE_HEIGHT))
        resized_image.save(filepath)
