from exchangelib.errors import ErrorFolderNotFound

from lib.action import BaseExchangeAction
from lib.utils import folder_to_dict


class ListFoldersAction(BaseExchangeAction):
    def run(self, root=None):
        if root is not None:
            try:
                folders = (self.account.inbox.parent / root).children
            except ErrorFolderNotFound:
                self.logger.error('Root folder not found: {}'.format(root))
                return False
        else:
            folders = self.account.inbox.parent.children

        return (True, [folder_to_dict(folder) for folder in folders])
