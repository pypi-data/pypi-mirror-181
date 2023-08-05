"""A variant of ABC that allows customizing the call behavior via _class_call()"""

__version__ = "1.1.0"

from callableabc.callableabc import CallableABC, CallableABCMeta, CallableABCMetaDict

__all__ = ("CallableABCMetaDict", "CallableABCMeta", "CallableABC")
