class APIException(Exception):
    """Wraps Exceptions thrown by the nOps API"""

    pass


class ImproperlyConfigured(Exception):
    """Configuration Errors"""

    pass


class PricingException(Exception):
    """Errors in the Pricing module."""

    pass


class RIExeption(Exception):
    """Errors in the RI module."""

    pass
