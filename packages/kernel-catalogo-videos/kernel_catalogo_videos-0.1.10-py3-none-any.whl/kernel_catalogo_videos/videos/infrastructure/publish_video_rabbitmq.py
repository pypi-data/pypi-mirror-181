# Apps
from kernel_catalogo_videos.core.infrastructure.rabbitmq import InterfaceRabbitMQ


class PublishCreatedVideoToQueue(InterfaceRabbitMQ):
    """
    Classe que inicializa as configurações do rabbitmq e a fila
    """

    def __init__(
        self,
        rabbitmq_conn,
        rabbitmq_channel,
        exchange,
        exchange_dlx,
        catalog_videos_dead,
        catalog_videos_dead_rk,
        catalog_videos,
        catalog_videos_rk,
    ):
        self.conn = rabbitmq_conn
        self.channel = rabbitmq_channel
        self.exchange = exchange
        self.exchange_dlx = exchange_dlx
        self.queue_dl = catalog_videos_dead
        self.routing_key_dl = catalog_videos_dead_rk
        self.queue = catalog_videos
        self.routing_key = catalog_videos_rk
        self.connect()
        super().__init__()
