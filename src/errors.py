class RepoWatcherError(Exception):
    """General class for handling exceptions."""


class InvalidRepositoryFormat(RepoWatcherError):
    """Exception raised for errors in the input method.

    Attributes:
        message -- explanation of the error
    """

    def __init__(
        self,
        message="Invalid repository pair format. Please use the format: user/repo or user/repo@branch",
    ):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message
