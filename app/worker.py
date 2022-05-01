import dramatiq
from dramatiq.brokers.rabbitmq import RabbitmqBroker

from service.upload_pages import upload_pages

rabbitmq_broker = RabbitmqBroker(host="rabbitmq")
dramatiq.set_broker(rabbitmq_broker)


@dramatiq.actor
def parse_pdf(filepath, document_id):
    upload_pages(document_id, filepath)
