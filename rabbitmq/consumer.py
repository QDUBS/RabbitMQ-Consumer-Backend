import os
import sys
from odoo.odoo import api
import pika
import json
import odoorpc
from utils.get_user import get_or_create_user
from utils.logger import LOGGER


SalesOrder = api.env['sale.order']
SaleOrderLine = api.env["sale.order.line"]


class SalesOrderConsumer:
    def __init__(self, url, queue) -> None:
        self.url = url
        self.connection = None
        self.channel = None
        self.connected = False
        self.queue = queue

    def connect(self):
        retry_count = 5
        LOGGER.info("Connecting to RabbitMQ...")
        while retry_count == 5 and retry_count > 0:
            try:
                connection_params = pika.URLParameters(url=self.url)
                self.connection = pika.BlockingConnection(connection_params)
                self.connected = True

            except pika.exceptions.ConnectionClosedByBroker:
                LOGGER.info("Connection closed by broker")
                retry_count -= 1

            except pika.exceptions.ProbableAccessDeniedError:
                LOGGER.info("Access denied")
                retry_count -= 1

            except pika.exceptions.AMQPChannelError:
                LOGGER.info("AMQP Channel Error")
                retry_count -= 1

            except pika.exceptions.AMQPChannelError:
                LOGGER.info("AMQP Channel Error")
                retry_count -= 1
            except pika.exceptions.AMQPConnectionError:
                LOGGER.info("AMQP Channel Error")
                retry_count -= 1

            except Exception as exec:
                LOGGER.info("Connection failed")
                retry_count -= 1

            return self.connection

        else:
            LOGGER.info("Connection failed")
            self.connected = False
            self.disconnect()
            return None

    def create_channel(self):
        if self.connection == None or self.connected == False:
            LOGGER.info("Connection not established")
            return None
        else:
            self.channel = self.connection.channel()

            # self.channel.exchange_declare(
            #     exchange='odoo_orders',
            #     exchange_type=pika.exchange_type,
            #     passive=False,
            #     durable=True,
            #     auto_delete=False)
            return self.channel

    def start_consuming(self):
        try:
            if self.channel == None:
                LOGGER.info("Channel not created")
                try:
                    self.connect()
                    self.create_channel()
                except Exception as exec:
                    raise exec
            else:
                self.channel.basic_consume(
                    queue=self.queue, on_message_callback=self.callback, auto_ack=True)
                LOGGER.info("Connected to RabbitMQ")
                LOGGER.info(' [*] Waiting for messages. To exit press CTRL+C')
                self.channel.start_consuming()
        except KeyboardInterrupt:
            LOGGER.info('Interrupted')
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)

    def disconnect(self):
        self.connection.close()

    def callback(self, ch, method, properties, body):
        data = json.loads(body)
        self.create_sales_order(data)

    def create_sales_order(self, data):
        email = data["email"]
        name = data["fullName"]
        phone = data["phone_number"]
        products = data["products"]

        try:
            user = get_or_create_user(name, email, phone)
            sale_order_id = SalesOrder.create({
                "partner_id": user["id"] if isinstance(user, dict) else user,
            })

            LOGGER.info("Creating sales order")
            for product in products:
                SaleOrderLine.create({
                    "name": product["product_name"],
                    "product_id": product["product_id"],
                    "order_id": sale_order_id,
                    "product_uom_qty": product["product_uom_qty"],
                    "price_unit": product["unit_price"]
                })

            SalesOrder.action_confirm(sale_order_id)
            LOGGER.info("Sales order created")

            LOGGER.info("*"*7)
            LOGGER.info("*"*7)
            LOGGER.info(' [*] Waiting for messages. To exit press CTRL+C')

            return True

        except odoorpc.error.RPCError as exc:
            LOGGER.info("Sales order creation failed")
            if exc.info["data"]["name"] == "odoo.exceptions.UserError":
                LOGGER.info(exc.info["data"]["message"])
                return False
            if exc.info["data"]["name"] == "odoo.exceptions.ValidationError":
                LOGGER.info(exc.info["data"]["message"])
                return False
            if exc.info["data"]["name"] == "odoo.exceptions.AccessError":
                LOGGER.info(exc.info["data"]["message"])
                return False
            if exc.info["data"]["name"] == "odoo.exceptions.MissingError":
                LOGGER.warning(exc.info["data"]["message"])
                return False
        except Exception as exec:
            LOGGER.info("Sales order creation failed, something went wrong")
            LOGGER.info(exec.info["data"]["message"])
            return False
