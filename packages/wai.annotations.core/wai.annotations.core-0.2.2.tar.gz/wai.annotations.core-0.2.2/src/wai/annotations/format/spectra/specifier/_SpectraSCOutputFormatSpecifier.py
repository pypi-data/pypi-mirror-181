from typing import Type, Tuple

from wai.annotations.core.component import Component
from wai.annotations.core.domain import DomainSpecifier
from wai.annotations.core.specifier import SinkStageSpecifier


class SpectraSCOutputFormatSpecifier(SinkStageSpecifier):
    """
    Specifier of the components for writing spectra from a spectrum classification dataset.
    """
    @classmethod
    def description(cls) -> str:
        return "Dummy writer that just outputs spectra from spectrum classification datasets."

    @classmethod
    def components(cls) -> Tuple[Type[Component], ...]:
        from wai.annotations.format.spectra.component import SpectraWriterSC
        return SpectraWriterSC,

    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        from wai.annotations.domain.spectra.classification import SpectrumClassificationDomainSpecifier
        return SpectrumClassificationDomainSpecifier
