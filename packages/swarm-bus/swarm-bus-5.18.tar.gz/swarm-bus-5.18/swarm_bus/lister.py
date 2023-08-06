"""
Lister of swarm-bus
"""
import logging

logger = logging.getLogger(__name__)


class Lister(object):
    """
    Lister logic
    """

    def list_queues(self, prefixes=None):
        """
        List registered queues
        """
        queues = []
        queue_prefix = self.transport.prefix

        for queue in self.client.list_queues(
                QueueNamePrefix=queue_prefix).get('QueueUrls', []):
            for prefix in prefixes or ['']:
                if '/%s%s' % (queue_prefix, prefix) in queue:
                    queues.append(queue)

        return queues

    def list_queues_detail(self, prefixes=None):
        """
        List registered queues in detail
        """
        queues = {}

        if prefixes:
            logger.info(
                '[%s] Getting details for queues : %s',
                self.log_namespace,
                ', '.join(prefixes),
            )
        else:
            logger.info(
                '[%s] Getting details for all queues',
                self.log_namespace,
            )
        for queue in self.list_queues(prefixes):
            try:
                response = self.client.get_queue_attributes(
                    QueueUrl=queue,
                    AttributeNames=['All'],
                )
                queues[queue] = response['Attributes']
            except self.client.exceptions.QueueDoesNotExist:
                pass

        return queues
