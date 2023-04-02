import inspect
from typing import (
    Any,
    Callable,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
    Tuple,
)


def prepare_arguments(
    func: Callable, arguments: Mapping[str, Any]
) -> Tuple[Sequence[Any], Mapping[str, Any]]:
    parameters: Mapping[str, inspect.Parameter] = inspect.signature(func).parameters

    args: MutableSequence[Any] = []
    kwargs: MutableMapping[str, Any] = {}

    parameter: inspect.Parameter
    for parameter in parameters.values():
        if parameter.name not in arguments:
            raise ValueError(f"Missing argument for parameter {parameter.name!r}")

        argument: Any = arguments[parameter.name]

        if parameter.kind == inspect.Parameter.POSITIONAL_ONLY:
            args.append(argument)
        elif parameter.kind in (
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
            inspect.Parameter.KEYWORD_ONLY,
        ):
            kwargs[parameter.name] = argument
        elif parameter.kind == inspect.Parameter.VAR_POSITIONAL:
            args.extend(argument)
        else:
            assert parameter.kind == inspect.Parameter.VAR_KEYWORD

            kwargs.update(argument)

    return (tuple(args), kwargs)
