from warnings import deprecated

from standalone_modules.shed_pi_module_utils.data_submission import (
    ReadingSubmissionService,
)


class BaseProtocol:
    def __init__(self, submission_service: ReadingSubmissionService):
        self.submission_service = submission_service

    def start(self) -> None:
        """
        Start any services or logic on demand
        """
        ...

    def stop(self) -> None:
        """
        Stop any services or logic on demand
        """
        ...

    def startup(self) -> None:
        """
        Run at startup
        """
        ...

    def shutdown(self) -> None:
        """
        Run at destruction
        """
        ...

    @deprecated("Deprecated run method is replaced by start")
    def run(self) -> None:
        raise NotImplementedError
