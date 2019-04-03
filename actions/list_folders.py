from base.action import BaseExchangeAction
from base import folder_to_dict


class ListFoldersAction(BaseExchangeAction):
    def run(self, root=None):
        if root:
            folders = self.account.root.glob('*/{}'.format(root)).folders
        else:
            folders = self.account.inbox.parent.children.folders

        return [folder_to_dict(folder) for folder in folders]
