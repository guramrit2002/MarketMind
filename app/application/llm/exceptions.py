class LLMError(Exception):
    """Raised when an LLM provider call fails.

    Vendor-specific errors are wrapped in this application-level error so
    callers stay independent of the concrete provider SDK.
    """


class LLMValidationError(LLMError):
    """Raised when an LLM response cannot be parsed or fails schema validation."""
