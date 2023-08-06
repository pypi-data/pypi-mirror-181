from typing import Type

from ....core.domain import DomainSpecifier
from ...classification import Classification
from .._Spectrum import Spectrum
from ._SpectrumClassificationInstance import SpectrumClassificationInstance

DESCRIPTION = """Spectra categorised by target.

The spectrum classification domain deals with labelling spectra as identifying a certain substance. Instances in this
domain contain a spectrum and a string label classifying the spectrum.
"""


class SpectrumClassificationDomainSpecifier(DomainSpecifier[Spectrum, Classification]):
    """
    Domain specifier for spectra annotated with a label
    classifying the contents of the spectrum.
    """
    @classmethod
    def name(cls) -> str:
        return "Spectrum Classification Domain"

    @classmethod
    def description(cls) -> str:
        return DESCRIPTION

    @classmethod
    def data_type(cls) -> Type[Spectrum]:
        return Spectrum

    @classmethod
    def annotations_type(cls) -> Type[Classification]:
        return Classification

    @classmethod
    def instance_type(cls) -> Type[SpectrumClassificationInstance]:
        return SpectrumClassificationInstance
