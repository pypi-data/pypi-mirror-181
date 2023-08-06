from __future__ import annotations


class ProviderNotImplementedError(NotImplementedError):
    """The provider name specified is not supported.

    This exception is raised when attempting to get a provider
    based on name that is not currently supported.
    """


class SMSNotImplementedError(NotImplementedError):
    """SMS is not implemented for the specified provider.

    This exception is raised when attempting to send a SMS message
    with a provider that does not have support for it.
    """


class MMSNotImplementedError(NotImplementedError):
    """MMS is not implemented for the specified provider.

    This exception is raised when attempting to send a MMS message
    with a provider that does not have support for it.
    """
