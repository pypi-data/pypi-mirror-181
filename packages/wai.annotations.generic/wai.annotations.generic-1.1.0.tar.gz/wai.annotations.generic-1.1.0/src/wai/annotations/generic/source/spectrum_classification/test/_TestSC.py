import os
from wai.annotations.core.component import SourceComponent
from wai.annotations.core.stream import ThenFunction, DoneFunction
from wai.annotations.domain.spectra import Spectrum
from wai.annotations.domain.spectra.classification import SpectrumClassificationInstance
from wai.annotations.domain.classification import Classification
from wai.common.cli.options import TypedOption


class TestSC(SourceComponent[SpectrumClassificationInstance]):

    input_dir: str = TypedOption(
        "--dir",
        type=str,
        default=".",
        help="the directory with the spec files"
    )

    def produce(
            self,
            then: ThenFunction[SpectrumClassificationInstance],
            done: DoneFunction
    ):
        """
        Produces elements and inserts them into the stream. Should call 'then'
        for each element produced, and then call 'done' when finished.

        :param then:    A function which forwards elements into the stream.
        :param done:    A function which closes the stream when called.
        """
        for f in os.listdir(self.input_dir):
            if not f.lower().endswith(".spec"):
                continue
            label = os.path.splitext(f)[0]
            full = os.path.join(self.input_dir, f)
            data = Spectrum.from_file(full)
            then(SpectrumClassificationInstance(data, Classification(label)))
        done()
