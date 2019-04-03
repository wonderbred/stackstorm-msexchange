from lib.action import BaseExchangeAction
from lib.utils import folder_to_dict


class GetFolderAction(BaseExchangeAction):
    def run(self, folder_name):
        result = self.account.root.glob('*/{}'.format(folder_name)).folders
        try:
            folder = result[0]
            return (True, folder_to_dict(folder))
        except IndexError:
            self.logger.error('Folder not found: {}'.format(folder_name))
            return False
