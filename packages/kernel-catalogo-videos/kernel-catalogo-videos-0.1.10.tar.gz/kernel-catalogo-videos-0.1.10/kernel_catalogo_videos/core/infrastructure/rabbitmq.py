"""
Modulo para definir tudo que represente uma ligação com o rabbitmq
"""
# Python
from abc import ABC, abstractmethod
from json import dumps
from typing import Dict

# Third
import pika
from pika import URLParameters, BlockingConnection


class RabbitMQ:
    """
    A class to do a connection
    """

    @staticmethod
    def connect(amqp_uri: str):
        """
        Connect sync to RabbitMQ and returns the connection and channel
        """
        params = URLParameters(amqp_uri)
        # number of socket connection attempts
        params.connection_attempts = 7
        # interval between socket connection attempts; see also connection_attempts.
        params.retry_delay = 300
        # AMQP connection heartbeat timeout value for negotiation during connection
        # tuning or callable which is invoked during connection tuning
        params.heartbeat = 600
        # None or float blocked connection timeout
        params.blocked_connection_timeout = 300
        try:
            connect = BlockingConnection(params)
            channel = connect.channel()

            return connect, channel

        except Exception as exc:
            raise exc


class InterfacePublishToQueue(ABC):
    """
    Interface to publish messages
    """

    conn = None
    channel = None
    exchange = None
    exchange_dlx = None
    queue_dl = None
    routing_key_dl = None
    queue = None
    routing_key = None

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def connect(self):
        """
        Abstract method to connect
        """
        pass

    @abstractmethod
    def publish(self, message: dict):
        """
        Abstract method to publish
        """
        pass

    def close_channel(self):
        """
        Close a channel
        """
        self.channel.close()

    def close_connection(self):
        """
        Close connection
        """
        self.conn.close()

    def teardown(self):
        """
        Closes a channel and connection
        """
        self.close_channel()
        self.close_connection()

    def run(self, message):
        """
        Connect and publish a message
        """
        self.connect()
        self.publish(message)

    def message_to_json(self, message: Dict):
        """ "
        Transforms a message dict to a json
        """
        try:
            body = dumps(message)
            return body
        except Exception as exc:
            raise exc


class InterfaceRabbitMQ(InterfacePublishToQueue):
    """
    Interface with connect and publish methods
    """

    def connect(self):
        if self.exchange_dlx and self.queue_dl and self.routing_key_dl:
            arguments = {
                "x-dead-letter-exchange": self.exchange_dlx,
                "x-dead-letter-routing-key": self.routing_key_dl,
            }
        else:
            arguments = {}

        self.channel.queue_declare(queue=self.queue, durable=True, arguments=arguments)
        self.channel.queue_bind(self.queue, self.exchange, routing_key=self.routing_key)
        # Turn on delivery confirmations
        self.channel.confirm_delivery()

    def publish(self, message: dict):
        """
        Publish a message in default exchange
        """

        properties = pika.BasicProperties(
            app_id="admin-catalog-video",
            content_type="application/json",
            delivery_mode=pika.DeliveryMode.Persistent,
        )

        body = self.message_to_json(message)

        # Send a message
        try:
            self.channel.basic_publish(
                exchange=self.exchange,
                routing_key=self.routing_key,
                body=body,
                properties=properties,
            )

        except pika.exceptions.UnroutableError as err:
            raise err
