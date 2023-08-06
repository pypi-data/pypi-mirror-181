from typing import Type

from ....core.domain import Instance
from ...classification import Classification
from .._Spectrum import Spectrum


class SpectrumClassificationInstance(Instance[Spectrum, Classification]):
    """
    An item in a spectrum-classification data-set.
    """
    @classmethod
    def data_type(cls) -> Type[Spectrum]:
        return Spectrum

    @classmethod
    def annotations_type(cls) -> Type[Classification]:
        return Classification
