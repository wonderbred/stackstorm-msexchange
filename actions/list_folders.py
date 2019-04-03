from base.action import BaseExchangeAction
from base import folder_to_dict


class ListFoldersAction(BaseExchangeAction):
    def run(self, root=None):
        if root is not None:
            result = self.account.root.glob('*/{}'.format(root)).folders
            try:
                parent = result[0]
            except IndexError:
                self.logger.error('Root folder not found: {}'.format(root))
                return False
        else:
            parent = self.account.inbox.parent.children.folders

        return (True, [folder_to_dict(folder) for folder in parent])
