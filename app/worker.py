from uuid import uuid4

import dramatiq
from PyPDF2 import PdfFileReader
from pdf2image import convert_from_path
from dramatiq.brokers.rabbitmq import RabbitmqBroker

from db import queries
from processing.process_page import get_page_path, resize_page_if_needed
from processing.process_document import get_document_path

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

    reader = PdfFileReader(document_path)
    pages_count = reader.numPages
    for page_number in range(1, pages_count + 1):

        # Process every page separately.
        process_image.send(document_id, page_number)

    # Update document status and number of pages.
    update_document_info.send(document_id, pages_count)


@dramatiq.actor()
def process_image(document_id, page_number):
    document_path = get_document_path(document_id)
    image = convert_from_path(document_path, first_page=page_number, last_page=page_number + 1)
    filepath = get_page_path(document_id, page_number)
    image[0].save(filepath, 'PNG')

    # Make image fit into given pixels rectangle.
    resize_page_if_needed(filepath)

    # Create DB entry.
    queries.create_page(document_id, filepath, page_number)


@dramatiq.actor
def update_document_info(document_id, pages_count):
    queries.update_document(document_id=document_id, num_of_pages=pages_count)
