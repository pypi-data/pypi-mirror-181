import asyncio
import functools
import inspect
import typing as t

from pydantic import BaseModel


class ServiceContainer(BaseModel):
    name: str
    service: t.Type
    args: tuple
    kwargs: dict


class Dependency:
    registry: t.List[ServiceContainer] = []

    @classmethod
    def add(cls, name: str, service: t.Type, *args, **kwargs) -> None:
        for container in cls.registry:
            if name == container.name:
                raise ValueError("Name duplicate addition.")

        cls.registry.append(ServiceContainer(name=name, service=service, args=args, kwargs=kwargs))

    @classmethod
    def get(cls, name: str) -> t.TypeVar("T"):
        for container in cls.registry:
            if name == container.name:
                return container.service(*container.args, **container.kwargs)

    @classmethod
    def override(cls, name: str, service: t.TypeVar("service"), *args, **kwargs) -> None:
        for container in cls.registry:
            if name == container.name:
                container.service = service
                container.args = args
                container.kwargs = kwargs

    @classmethod
    def iterate(cls, sig: inspect.Signature) -> t.Iterator[ServiceContainer]:
        for parameter in sig.parameters.values():
            name = parameter.annotation.__name__ if isinstance(parameter.annotation, type) else parameter.annotation
            yield from filter(lambda container: name == container.name, cls.registry)

    @classmethod
    def inject(cls) -> t.Any:
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                sig = inspect.signature(func)
                for container in cls.iterate(sig):
                    args += (container.service(*container.args, **container.kwargs),)

                return func(*args, **kwargs)

            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs):
                sig = inspect.signature(func)
                for container in cls.iterate(sig):
                    args += (container.service(*container.args, **container.kwargs),)

                return await func(*args, **kwargs)

            if asyncio.iscoroutinefunction(func):
                return async_wrapper

            return wrapper

        return decorator
