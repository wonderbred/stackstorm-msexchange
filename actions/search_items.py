from lib.action import BaseExchangeAction
from lib.utils import item_to_dict


class SearchItemsAction(BaseExchangeAction):
    def run(self, folder, include_body, include_text_body, unread_only,
            subject=None):
        q = self.account.inbox.parent / folder
        if subject:
            q = q.filter(subject__icontains=subject)
        if unread_only:
            q = q.filter(is_read=False)
        items = q.all()

        return [item_to_dict(item, include_body=include_body,
                             include_text_body=include_text_body) for item in
                items]
