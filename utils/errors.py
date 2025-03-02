
class ValidationError(Exception):
    pass

class LegalErrorHandler:
    def handle(self, error):
        if isinstance(error, ValidationError):
            return "Our legal team needs to review this question. Please try rephrasing."
        return "A legal system error occurred. Our team has been notified."