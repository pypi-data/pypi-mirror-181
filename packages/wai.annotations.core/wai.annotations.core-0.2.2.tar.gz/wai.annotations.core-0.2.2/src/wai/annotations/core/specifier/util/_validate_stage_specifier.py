from typing import Any

from ...component import *
from .._StageSpecifier import StageSpecifier
from .._ProcessorStageSpecifier import ProcessorStageSpecifier
from .._SinkStageSpecifier import SinkStageSpecifier
from .._SourceStageSpecifier import SourceStageSpecifier


def type_name(value: Any) -> str:
    """
    Gets the type-name of the value's type, or of the value itself
    if it is a type.

    :param value:
                The value or type to get the name of.
    :return:
                The name.
    """
    return (
        value.__qualname__ if isinstance(value, type)
        else type(value).__qualname__
    )


def validate_stage_specifier(specifier):
    """
    Ensures that a stage specifier has been properly configured.

    :param specifier:   The specifier to check.
    """

    if not isinstance(specifier, type) or not issubclass(specifier, StageSpecifier):
        raise Exception(f"Not a stage specifier ({type_name(specifier)})")

    components = specifier.components()

    # Make sure the components are a tuple
    if not isinstance(components, tuple):
        raise Exception("Components not specified as a tuple")

    # Make sure at least one component is specified
    if len(components) == 0:
        raise Exception("No components specified")

    if issubclass(specifier, SourceStageSpecifier):
        if not isinstance(components[0], type) or not issubclass(components[0], SourceComponent):
            raise Exception(f"Source stage must begin with source component ({type_name(components[0])})")
        for component in components[1:]:
            if not isinstance(component, type) or not issubclass(component, ProcessorComponent):
                raise Exception(f"All subsequent components of a source stage must be processors ({type_name(component)})")

    elif issubclass(specifier, ProcessorStageSpecifier):
        for component in components:
            if not isinstance(component, type) or not issubclass(component, ProcessorComponent):
                raise Exception(f"Processor stage can only consist of processor components ({type_name(component)})")

    elif issubclass(specifier, SinkStageSpecifier):
        for component in components[:-1]:
            if not isinstance(component, type) or not issubclass(component, ProcessorComponent):
                raise Exception(f"All preceding components of a sink stage must be processors ({type_name(component)})")
        if not isinstance(components[-1], type) or not issubclass(components[-1], SinkComponent):
            raise Exception(f"Sink stage must end with sink component ({type_name(components[-1])})")

    else:
        raise Exception("Unknown stage specifier type")
