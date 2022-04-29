import dramatiq
from dramatiq.brokers.rabbitmq import RabbitmqBroker


rabbitmq_broker = RabbitmqBroker(host="rabbitmq")
dramatiq.set_broker(rabbitmq_broker)


@dramatiq.actor
def parse_pdf():
    import time
    time.sleep(3)
    print("DONEEEEEEEEEEEEEEEEEE")
    return "Done"
