from typing import Type, Tuple

from wai.annotations.core.component import Component
from wai.annotations.core.domain import DomainSpecifier
from wai.annotations.core.specifier import SinkStageSpecifier


class SpectrumClassificationSinkSpecifier(SinkStageSpecifier):
    """
    Specifies the generic spectrum classification sink.
    """
    @classmethod
    def description(cls) -> str:
        return "Generic spectrum classification sink."

    @classmethod
    def components(cls) -> Tuple[Type[Component], ...]:
        from wai.annotations.generic.sink.base.component import BaseSink
        return BaseSink,

    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        from wai.annotations.domain.spectra.classification import SpectrumClassificationDomainSpecifier
        return SpectrumClassificationDomainSpecifier
