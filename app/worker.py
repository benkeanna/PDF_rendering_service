import os

import dramatiq
from dramatiq.brokers.rabbitmq import RabbitmqBroker
from pdf2image import convert_from_path

from service.upload_pages import pages_folder

rabbitmq_broker = RabbitmqBroker(host="rabbitmq")
dramatiq.set_broker(rabbitmq_broker)


@dramatiq.actor
def parse_pdf(filepath, document_id):
    images = convert_from_path(filepath)

    for i in range(len(images)):
        filename = 'page' + str(i) + '.png'
        filepath = os.path.join(pages_folder(document_id), filename)
        images[i].save(filepath, 'PNG')

    return "Done"
