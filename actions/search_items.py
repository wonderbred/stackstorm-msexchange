from base.action import BaseExchangeAction
from base import item_to_dict


class SearchItemsAction(BaseExchangeAction):
    def run(self, folder, include_body, unread_only, subject=None):
        q = self.account.inbox.parent / folder
        if subject:
            q = q.filter(subject__contains=subject)
        if unread_only:
            q = q.filter(is_read=False)
        items = q.all()

        return [item_to_dict(item, include_body=include_body) for item in items]
