import typing
from abc import ABCMeta, abstractmethod
from collections.abc import Awaitable
from typing import Generic, TypeVar

from selva.di.inject import Inject

T = TypeVar("T")
N = TypeVar("N", bound=str)


def _is_service_dependency(value) -> bool:
    return isinstance(value, Inject) or value is Inject


class ServiceMeta(ABCMeta):
    def __new__(
        mcs,
        clsname,
        bases,
        namespace,
        *,
        provides: type = None,
        name: str = None,
        **kwargs,
    ):
        cls = super().__new__(mcs, clsname, bases, namespace)
        cls._name_ = name

        def _pred(base):
            return (base.__module__ == mcs.__module__) and (
                base.__qualname__ == "Service"
            )

        # if any(filter(_pred, bases)) and (
        #     args := typing.get_args(cls.__orig_bases__[0])
        # ):
        for orig_base in getattr(cls, "__orig_bases__", []):
            origin = typing.get_origin(orig_base)
            if origin.__module__ == mcs.__module__ and origin.__qualname__ == "Service":
                args = typing.get_args(orig_base)
                if args != (T,):
                    cls._provides_ = args[0]

        return cls


class Service(Generic[T], metaclass=ServiceMeta):
    provides: type = None
    name: str = None

    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls)

        for arg, val in kwargs.items():
            if arg in cls.__di_dependencies__:
                setattr(obj, arg, val)
            else:
                raise TypeError(
                    f"Service '{cls.__qualname__}' does not have dependency '{arg}'"
                )

        return obj

    def initialize(self) -> Awaitable | None:
        pass

    def finalize(self) -> Awaitable | None:
        pass


class ServiceFactoryMeta(ServiceMeta):
    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)

        def _pred(base):
            return (base.__module__ == mcs.__module__) and (
                base.__qualname__ == "ServiceFactory"
            )

        if any(filter(_pred, bases)) and (
            typing.get_args(cls.__orig_bases__[0]) == (T,)
        ):
            raise TypeError("Missing generic parameter")

        return cls


class ServiceFactory(Generic[T], metaclass=ServiceFactoryMeta):
    @abstractmethod
    def create(self) -> T | Awaitable[T]:
        raise NotImplementedError()

    def finalize(self, instance: T) -> Awaitable | None:
        pass


class Test(Service[int], name="int", provides=int):
    pass
