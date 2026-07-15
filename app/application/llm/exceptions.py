class LLMError(Exception):
    """Raised when an LLM provider call fails.

    Vendor-specific errors are wrapped in this application-level error so
    callers stay independent of the concrete provider SDK.
    """
