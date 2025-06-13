class FileFormatNotSupportedError(Exception):
    """
    Exception raised when a file format is not supported.
    """

    def __init__(self, file_format: str, message: str = "File format not supported"):
        self.file_format = file_format
        self.message = f"{message}: {file_format}"
        super().__init__(self.message)


class SeviceNotConfiguredError(Exception):
    """
    Exception raised when a service is not configured.
    """

    def __init__(self, service_name: str, message: str = "Service not configured"):
        self.service_name = service_name
        self.message = f"{message}: {service_name}"
        super().__init__(self.message)


class WhileProcessingError(Exception):
    """
    Exception raised when an error occurs while processing a file.
    """

    def __init__(self, message: str = "Error while processing"):
        self.message = message
        super().__init__(self.message)
