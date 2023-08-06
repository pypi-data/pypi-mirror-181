from typing import Type, Tuple

from wai.annotations.core.component import Component
from wai.annotations.core.domain import DomainSpecifier
from wai.annotations.core.specifier import SourceStageSpecifier


class SpectraSCInputFormatSpecifier(SourceStageSpecifier):
    """
    Specifier of the components for turning spectra into a spectrum classification dataset.
    """
    @classmethod
    def description(cls) -> str:
        return "Dummy reader that turns spectra into a spectrum classification dataset."

    @classmethod
    def components(cls) -> Tuple[Type[Component], ...]:
        from wai.annotations.core.component.util import LocalFilenameSource
        from wai.annotations.format.spectra.component import SpectraReaderSC
        return LocalFilenameSource, SpectraReaderSC

    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        from wai.annotations.domain.spectra.classification import SpectrumClassificationDomainSpecifier
        return SpectrumClassificationDomainSpecifier
