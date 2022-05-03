from uuid import uuid4

import dramatiq
from PyPDF2 import PdfFileReader
from dramatiq import group
from pdf2image import convert_from_path
from dramatiq.brokers.rabbitmq import RabbitmqBroker
from dramatiq.results.backends import RedisBackend
from dramatiq.results import Results

from db import queries
from config import Config
from utils.document import get_document_path
from utils.page import get_page_path, resize_page_if_needed

rabbitmq_broker = RabbitmqBroker(host="rabbitmq")
result_backend = RedisBackend(url='redis://redis')
rabbitmq_broker.add_middleware(Results(backend=result_backend))
dramatiq.set_broker(rabbitmq_broker)


def upload_document(file):
    # Save file to appropriate path.
    document_id = str(uuid4())
    filepath = get_document_path(document_id)
    file.save(filepath)

    # Create DB entry.
    queries.create_document(document_id=document_id, filepath=filepath)

    # Process document pages.
    upload_pages.send(document_id)

    return document_id


@dramatiq.actor(store_results=True)
def upload_pages(document_id):
    document_path = get_document_path(document_id)

    reader = PdfFileReader(document_path)
    pages_count = reader.numPages

    process_image_tasks = []
    for page_number in range(1, pages_count + 1):

        # Process every page separately.
        item = process_image.message(document_id, page_number)
        process_image_tasks.append(item)

    result = group(process_image_tasks).run(delay=500)

    task_timeout_in_ms = 60 * 60 * 1000
    result.wait(timeout=task_timeout_in_ms)

    # Logger should replace prints and there should be more logs in general.
    print('Done')

    # Update document status and number of pages.
    update_document_info.send(document_id, pages_count)


@dramatiq.actor(store_results=True)
def process_image(document_id, page_number):
    print(f'Processing page {page_number}')

    document_path = get_document_path(document_id)
    image = convert_from_path(document_path, first_page=page_number, last_page=page_number + 1)
    page_path = get_page_path(document_id, page_number)
    image[0].save(page_path, Config.PAGE_EXTENSION.upper())

    print(f'Resizing image {page_path}')
    # Make image fit into given pixels rectangle.
    resize_page_if_needed(page_path)

    print(f'Storing page {page_number} into DB')
    # Create DB entry.
    queries.create_page(document_id, page_path, page_number)


@dramatiq.actor(store_results=True)
def update_document_info(document_id, pages_count):
    queries.finalize_document(document_id=document_id, num_of_pages=pages_count)
