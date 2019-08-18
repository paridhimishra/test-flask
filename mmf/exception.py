class Error(Exception):
    def __init__(self, message, errors):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)

        # Now for your custom code...
        self.errors = errors


class SchedulerNotFoundError(Error):
    pass


class ModelNotFoundError(Error):
    pass


class SchedulerNotRunningError(Error):
    pass


class ModelRunFailedError(Error):
    pass


class ModelNotFoundError(Error):
    pass

