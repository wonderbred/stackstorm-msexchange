from exchangelib.errors import ErrorItemNotFound

from lib.action import BaseExchangeAction
from lib.utils import item_to_dict


class GetItemAction(BaseExchangeAction):
    def run(self, item_id, folder):
        folder = self.account.inbox.parent / folder
        item = folder.get(id=item_id)
        try:
            assert type(item) != ErrorItemNotFound
            self.logger.debug('Item(id="{}") found'.format(item_id))
        except AssertionError:
            return False, 'Item(id="{}") not found'.format(item_id)

        return (True, item_to_dict(item, include_body=True,
                                   include_text_body=True))
