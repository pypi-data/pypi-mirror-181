from .nubium_table_app import NubiumTableApp
from fluvii.exceptions import NoMessageError, PartitionsAssigned
from fluvii.transaction import TableTransaction
import logging

LOGGER = logging.getLogger(__name__)


class EloquaRetrieverTransaction(TableTransaction):
    """
    Necessary because we aren't usually consuming a message while producing table messages. We can mock out what
    we would need from a message by returning static values for the necessary items called.
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


class NubiumEloquaRetrieverApp(NubiumTableApp):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, transaction_cls=EloquaRetrieverTransaction)

    def _handle_message(self, **kwargs):
        self.consume(**kwargs)
        timestamp = self.transaction.value()['timestamp']
        LOGGER.info(f'External timestamp update received: {timestamp} UTC')
        self.transaction.update_table_entry(timestamp)

    def _no_message_callback(self):
        self._producer.poll(0)
        if len(self._rebalance_manager._all_partitions) == 2:
            self.app_function(self.transaction, *self.app_function_arglist)
            self._finalize_app_batch()
        else:
            LOGGER.debug('Waiting on rebalance to complete...')

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
