from typing import Type

from ....core.domain import DomainSpecifier

from ._VoidOutputFormatSpecifier import VoidOutputFormatSpecifier


class VoidSCOutputFormatSpecifier(VoidOutputFormatSpecifier):
    """
    Specifier for the void-writer in the spectrum-classification domain.
    """
    @classmethod
    def description(cls) -> str:
        return "Consumes spectrum classification instances without writing them."

    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        from wai.annotations.domain.spectra.classification import SpectrumClassificationDomainSpecifier
        return SpectrumClassificationDomainSpecifier
