from standalone_modules.shed_pi_module_utils.data_submission import (
    ReadingSubmissionService,
)


class BaseProtocol:
    def __init__(self, submission_service: ReadingSubmissionService):
        self.submission_service = submission_service

    def stop(self):
        ...

    def startup(self):
        ...

    def run(self):
        raise NotImplementedError

    def shutdown(self):
        ...
