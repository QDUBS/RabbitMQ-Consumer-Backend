# from dotenv import load_dotenv
import os
import sys

from rabbitmq.consumer import SalesOrderConsumer
from utils.logger import LOGGER


rabbitmq_url = os.environ.get("CLOUD_AMPQ_URL")


def main():
    LOGGER.info("Starting the app")
    if not rabbitmq_url:
        raise Exception("CLOUD_AMPQ_URL not set")

    connetion = SalesOrderConsumer(url=rabbitmq_url, queue="odoo_orders")
    connetion.connect()
    connetion.create_channel()
    connetion.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        LOGGER.warning("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
    except Exception as exec:
        LOGGER.info(exec)
        os._exit(0)
