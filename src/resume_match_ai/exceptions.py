class RateLimitError(Exception):
    def __init__(self, message="Too many requests! Please try again tomorrow.") -> None:
        self.message = message

class RequestError(Exception):
    def __init__(self, message="Unexpected error encounter on rate limiter.") -> None:
        self.message = message
