from uuid import uuid4

import dramatiq
from PIL import ImageOps
from PIL import Image
from pdf2image import convert_from_path
from dramatiq.brokers.rabbitmq import RabbitmqBroker

from config import Config
from db import queries
from service.upload_page import get_page_path
from service.upload_document import get_document_path

rabbitmq_broker = RabbitmqBroker(host="rabbitmq")
dramatiq.set_broker(rabbitmq_broker)


def upload_document(file):
    # Save file to appropriate path.
    document_id = str(uuid4())
    filepath = get_document_path(document_id)
    file.save(filepath)

    # Create DB entry.
    queries.create_document(document_id=document_id, filepath=filepath)

    # Queue document processing.
    upload_pages.send(document_id)

    return document_id


@dramatiq.actor
def upload_pages(document_id):

    document_path = get_document_path(document_id)
    images = convert_from_path(document_path)

    for page_number in range(len(images)):
        filepath = get_page_path(document_id, page_number)
        images[page_number].save(filepath, 'PNG')
        resize_if_needed(filepath)

        queries.create_page(document_id, filepath, page_number)

    # Update document status and number of pages.
    queries.update_document(document_id=document_id, num_of_pages=len(images))


def resize_if_needed(filepath):
    image = Image.open(filepath)
    resized_image = ImageOps.contain(image, (Config.MAX_PAGE_WIDTH, Config.MAX_PAGE_HEIGHT))
    resized_image.save(filepath)
