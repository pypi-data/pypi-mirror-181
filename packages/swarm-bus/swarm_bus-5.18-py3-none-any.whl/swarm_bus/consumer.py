"""
Consumer for swarm-bus
"""
import base64
import json
import logging
import time
from concurrent import futures

logger = logging.getLogger(__name__)


class Consumer(object):
    """
    Consumer logic
    """
    max_threads = 1
    polling_messages = 10

    polled_messages = 0
    last_polling_time = None
    last_processed_time = None
    start_consume_time = None
    end_consume_time = None

    def consume(self, queue_name, callback=None, error_handler=None,
                polling_messages=10, max_messages=100000,
                pre_polling_handler=None, post_polling_handler=None):
        """
        Consume message datas
        """
        self.polling_messages = polling_messages

        queue_set = self.get_queue_set(queue_name)

        if callback is None:
            raise ValueError(
                'callback parameter can not be empty',
            )

        callback_wrapped = self.callback_wrapper(callback, error_handler)

        self.start_consume_time = time.time()

        while max_messages > 0:
            sleep_time = self.next_consume_time
            if sleep_time:
                logger.debug(
                    '[%s] Consuming is on hold. Next try in %s seconds',
                    self.log_namespace,
                    sleep_time,
                )
            else:
                if pre_polling_handler:
                    pre_polling_handler(max_messages)

                polled = self.polling(
                    queue_set, callback_wrapped,
                    self.polling_messages,
                )

                self.last_polling_time = time.time()

                if post_polling_handler:
                    post_polling_handler(max_messages, polled)

                max_messages -= polled
                self.polled_messages += polled

                sleep_time = queue_set.sleep_time
                if sleep_time:
                    logger.debug(
                        '[%s] Queue sleeping for %s seconds',
                        self.log_namespace,
                        sleep_time,
                    )

            time.sleep(sleep_time)

        self.end_consume_time = time.time()

        logger.debug(
            '[%s] Stop consuming messages',
            self.log_namespace,
        )

    @property
    def next_consume_time(self):
        """
        Check a queue can be consumed.
        """
        return 0

    def polling(self, queue_set, callback_wrapped, polling_messages):
        """
        Poll all the messages availables for each priorities
        """
        total_polled = 0

        for queue_priority in queue_set.queues:
            logger.debug(
                '[%s] Polling %s for %s seconds',
                self.log_namespace,
                queue_priority.url,
                queue_set.polling_interval,
            )
            polled_messages = queue_priority.receive_messages(
                WaitTimeSeconds=queue_set.polling_interval,
                MaxNumberOfMessages=polling_messages,
            )
            polled = len(polled_messages)
            logger.debug(
                '[%s] %s messages polled',
                self.log_namespace,
                polled,
            )
            total_polled += polled

            if self.max_threads > 1 and polled > 1:
                logger.debug(
                    '[%s] Use %s threads for %s messages',
                    self.log_namespace,
                    self.max_threads,
                    polled,
                )
                with futures.ThreadPoolExecutor(
                        max_workers=self.max_threads,
                ) as executor:
                    [
                        executor.submit(
                            callback_wrapped,
                            self.decode_body(message),
                            message,
                        )
                        for message in polled_messages
                    ]
            else:
                for message in polled_messages:
                    body = self.decode_body(message)

                    callback_wrapped(
                        body,
                        message,
                    )

            if polled:
                self.last_processed_time = time.time()

        return total_polled

    def decode_body(self, message):
        """
        Decode the message body for having a dict
        """
        try:
            return json.loads(message.body)
        except ValueError:
            # Old bus compatibility
            return json.loads(
                base64.b64decode(
                    json.loads(
                        base64.b64decode(
                            message.body,
                        ).decode('utf8'),
                    )['body'],
                ).decode('utf8'),
            )

    def callback_wrapper(self, callback, error_handler):
        """
        Decorate the callback to log exceptions
        and send them to Senty later if possible.

        Also cancels the exception to avoid process to crash !
        """
        def exception_catcher(body, message):
            """
            Decorator around callback.
            """
            try:
                return callback(body, message)
            except Exception:
                logger.exception(
                    '[%s] Unhandled exception occured !',
                    self.log_namespace,
                )
                if error_handler:
                    error_handler(body, message)
                    logger.debug(
                        '[%s] Error handler called',
                        self.log_namespace,
                    )

        return exception_catcher
