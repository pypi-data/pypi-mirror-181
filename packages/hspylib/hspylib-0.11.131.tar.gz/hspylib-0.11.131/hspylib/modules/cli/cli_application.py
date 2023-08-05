from hspylib.core.enums.exit_status import ExitStatus
from hspylib.modules.application.application import Application
from hspylib.modules.application.version import Version


class CliApplication(Application):
    """TODO"""

    def _setup_arguments(self) -> None:
        pass

    def _main(self, *params, **kwargs) -> ExitStatus:
        pass

    def _cleanup(self) -> None:
        pass

    def __init__(self, name: str, version: Version):
        super().__init__(name, version)
