from io import StringIO
from typing import Dict, Optional

from wai.common.file.spec import Spectrum as SpectrumBase
from wai.common.file.spec import read_spectrum

from ...core.domain import Data


class Spectrum(Data):
    """
    Contains the information about a spectrum in a data-set.
    """
    def __init__(
            self,
            filename: str,
            data: Optional[bytes] = None
    ):
        super().__init__(filename, data)

        self._spectrum_base: SpectrumBase = (
            read_spectrum(StringIO(data.decode("utf-8"))) if data is not None
            else SpectrumBase()
        )

    def __str__(self):
        return str(self._spectrum_base)

    @classmethod
    def from_file_data(cls, file_name: str, file_data: bytes) -> 'Spectrum':
        return cls(file_name, file_data)
