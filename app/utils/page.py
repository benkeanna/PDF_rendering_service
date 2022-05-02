import os

from PIL import Image, ImageOps

from config import Config


def pages_folder(document_id):
    """Returns folder name in format: 'path-to-data/data/<document_id>/pages'."""
    folder_path = os.path.join(Config.UPLOAD_FOLDER, str(document_id), Config.PAGES_FOLDER_NAME)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    return folder_path


def get_page_path(document_id, page_number):
    filename = f'page{str(page_number)}.{Config.PAGE_EXTENSION}'
    filepath = os.path.join(pages_folder(document_id), filename)
    return filepath


def resize_page_if_needed(filepath):
    image = Image.open(filepath)
    resized_image = ImageOps.contain(image, (Config.MAX_PAGE_WIDTH, Config.MAX_PAGE_HEIGHT))
    resized_image.save(filepath)