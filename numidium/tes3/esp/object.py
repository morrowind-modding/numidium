from __future__ import annotations

from typing import Any

from .. import _tes3  # type: ignore

WRAPPERS: dict[type, type] = {}


class TES3Meta(type):
    def __new__(cls, name: str, bases: tuple[type, ...], namespace: dict[str, Any]) -> type:

        # optimize slots
        namespace["__slots__"] = ("_wrapped",)

        # create the type
        ty = super().__new__(cls, name, bases, namespace)

        # set wrapped type
        if wrapped := vars(_tes3).get(name):
            WRAPPERS[wrapped] = ty

        return ty


class TES3Object(metaclass=TES3Meta):
    _wrapped: object

    def __getattr__(self, name: str) -> Any:
        return getattr(self._wrapped, name)

    def __repr__(self) -> str:
        fields = ", ".join(
            f"{name}={getattr(self, name)}"
            for name in self.annotations
        )  # fmt: skip
        return f"{self.type_name}({fields})"

    @staticmethod
    def wrap(source: Any) -> TES3Object:
        cls: type = WRAPPERS[type(source)]
        instance: TES3Object = cls.__new__(cls)  # type: ignore[call-overload]
        instance._wrapped = source
        return instance

    @property
    def type_name(self) -> str:
        return type(self).__name__

    @property
    def annotations(self) -> dict[str, str]:
        return type(self).__annotations__
