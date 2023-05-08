class ServiceMessage:
    def __init__(self, content=None, errors=None):
        if errors is None:
            errors = []
        self.content = content
        self.errors = errors
