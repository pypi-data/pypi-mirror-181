from wai.annotations.core.component import SinkComponent
from wai.annotations.core.component.util import AnnotationFileProcessor
from wai.annotations.core.stream import ThenFunction
from wai.annotations.domain.classification import Classification
from wai.annotations.domain.spectra import Spectrum
from wai.annotations.domain.spectra.classification import SpectrumClassificationInstance
from wai.common.cli.options import TypedOption


class SpectraReaderSC(AnnotationFileProcessor[SpectrumClassificationInstance]):
    """
    Dummy reader that turns a list of spectra into a spectrum classification dataset.
    """
    def read_annotation_file(self, filename: str, then: ThenFunction[SpectrumClassificationInstance]):
        then(
            SpectrumClassificationInstance(
                Spectrum.from_file(filename),
                Classification("?")
            )
        )

    def read_negative_file(self, filename: str, then: ThenFunction[SpectrumClassificationInstance]):
        then(
            SpectrumClassificationInstance(
                Spectrum.from_file(filename),
                None
            )
        )


class SpectraWriterSC(
    SinkComponent[SpectrumClassificationInstance]
):
    """
    Writes the spectra to the specified output directory.
    """
    output_dir: str = TypedOption(
        "-o", "--output-dir",
        type=str,
        default=".",
        help="the directory to write the spectra to"
    )

    def consume_element(self, element: SpectrumClassificationInstance):
        element.data.write_data_if_present(self.output_dir)

    def finish(self):
        pass

