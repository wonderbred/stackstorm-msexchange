from exchangelib.errors import ErrorItemNotFound

from lib.action import BaseExchangeAction


class MoveItemsAction(BaseExchangeAction):
    def run(self, item_ids, from_folder, to_folder, mark_read):
        from_folder = self.account.inbox.parent / from_folder
        to_folder = self.account.inbox.parent / to_folder
        i = 0
        for item_id in item_ids:
            item = from_folder.get(id=item_id)
            try:
                assert type(item) != ErrorItemNotFound
                self.logger.debug('Item found')
            except AssertionError:
                return False, 'Item(id="{}") not found'.format(item_id)
            if mark_read:
                self.mark_item_read(item)
                self.logger.debug('Item(id="{}") marked read'.format(item_id))
            item.move(to_folder=to_folder)
            self.logger.info(
                'Item(subject="{}") moved to "{}"'.format(item.subject,
                                                          to_folder))
            i += 1

        return (True, '{} items moved from "{}" to "{}"'.format(i, from_folder,
                                                                to_folder))
