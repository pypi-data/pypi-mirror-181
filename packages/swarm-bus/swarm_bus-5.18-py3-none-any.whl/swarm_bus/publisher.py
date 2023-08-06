"""
Publisher for swarm-bus
"""
import logging

logger = logging.getLogger(__name__)


class Publisher(object):
    """
    Publisher logic
    """

    def publish(self, queue_name, datas, priority=0,
                delay=0, attributes=None):
        """
        Publish message datas into queue
        """
        if attributes:
            attributes = attributes.copy()
        else:
            attributes = {}
        queue = self.get_queue_lazy(queue_name, priority)

        queue.send_message(
            MessageBody=datas,
            MessageAttributes=attributes,
            DelaySeconds=delay,
        )

        logger.info(
            "[%s] Message published on '%s'",
            self.log_namespace,
            queue.url,
        )
