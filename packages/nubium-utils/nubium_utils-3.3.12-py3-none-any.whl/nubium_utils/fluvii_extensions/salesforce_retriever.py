from fluvii.exceptions import PartitionsAssigned, NoMessageError
from fluvii.fluvii_app.fluvii_table_app import TableTransaction
from .nubium_table_app import NubiumTableApp
import logging


LOGGER = logging.getLogger(__name__)


class SalesforceRetrieverTransaction(TableTransaction):
    """
    Necessary because we aren't usually consuming a message while producing table messages. We can mock out what
    that message is.
    """
    def key(self):
        return 'timestamp'

    def headers(self):
        try:
            return super().headers()
        except Exception:
            return {'guid': 'none', 'last_updated_by': 'self'}

    def partition(self):
        return 0


class NubiumSalesforceRetrieverApp(NubiumTableApp):
    def __init__(self, app_function, consume_topic, produce_topic_schema_dict, app_function_arglist=None):
        super().__init__(app_function, consume_topic,
                         produce_topic_schema_dict=produce_topic_schema_dict, app_function_arglist=app_function_arglist,
                         transaction_cls=SalesforceRetrieverTransaction)

    # def _app_run(self, *args, **kwargs):
    #     self.producer.poll(0)
    #     self.transaction._refresh_transaction_fields()
    #     self.app_function(self.transaction, *self.app_function_arglist)
    #     self._shutdown = True
    #     LOGGER.info('stopping event loop...')
    #     self.transaction.event_loop.stop()

    def _handle_message(self):
        self.producer.poll(0)
        self.transaction._init_attrs()
        self.app_function(self.transaction, *self.app_function_arglist)  # this app doesn't loop, its a one time call
        self._shutdown = True  #
        LOGGER.info('stopping event loop...')
        self.transaction.event_loop.stop()

    def _run(self, **kwargs):
        unassigned = True
        while unassigned:
            try:
                self.consume(**kwargs)
            except NoMessageError:
                self._no_message_callback()
            except PartitionsAssigned:
                unassigned = False
                self._handle_rebalance()
        super()._run(**kwargs)


# def _app_run(self, *args, **kwargs):
#     if not self.transaction.message or self.transaction._committed:
#         self.consume(*args, **kwargs)
#         self.app_function(self.transaction, *self.app_function_arglist)
#     self.commit()
#
#
# def _app_run_loop(self, *args, **kwargs):
#     while not self._shutdown:
#         try:
#             LOGGER.debug('Running app function...')
#             self._app_run(*args, **kwargs)
#         except NoMessageError:
#             self.producer.poll(0)
#             LOGGER.info('No messages!')
#         except GracefulTransactionFailure:
#             LOGGER.info("Graceful transaction failure; retrying message with a new transaction...")
#             self.transaction.abort_active_transaction()
#         except FatalTransactionFailure:
#             LOGGER.info("Fatal transaction failure; recreating the producer and retrying message...")
#             self.transaction.abort_active_transaction()
#             self.reset_gtfo_producer()