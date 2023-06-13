#  未应用，开发中

from damai.configs import Configs
from damai.engine import ExecutionEngine


class Runner:

    def __init__(self, configs=None):

        if isinstance(configs, dict) or configs is None:
            self.configs = Configs(configs)

        self.engine = ExecutionEngine()
