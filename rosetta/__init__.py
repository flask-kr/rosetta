import os

from framework import Environment
from framework import ServerManager as BaseServerManager
from framework import CommandManager as BaseCommandManager

os.environ['APP_DIR'] = os.path.dirname(os.path.realpath(__file__))

class ServerManager(BaseServerManager):
    def __init__(self):
        super(ServerManager, self).__init__()
        self.env.load_config_file('$APP_DIR/data/base_config.yml')

class CommandManager(BaseCommandManager):
    def __init__(self):
        super(CommandManager, self).__init__()
        self._server_manager = None

    @property
    def server_manager(self):
        if self._server_manager is None:
            self._server_manager = ServerManager()

            try:
                self._server_manager.env.load_config_file('$PWD/active_config.yml')
            except Environment.Error:
                print "#### no active config"
                print "\t./mange switch_config rosetta/data/$(TARGET)_config.yml"
                raise self.Error('NO_ACTIVE_CONFIG')

            self._server_manager.create_all()

        return self._server_manager
