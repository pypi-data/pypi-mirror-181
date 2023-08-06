from typing import Type, Tuple

from wai.annotations.core.component import ProcessorComponent
from wai.annotations.core.domain import DomainSpecifier
from wai.annotations.core.specifier import ProcessorStageSpecifier


class SpectrumClassificationISPSpecifier(ProcessorStageSpecifier):
    """
    Specifies the generic spectrum classification ISP.
    """
    @classmethod
    def description(cls) -> str:
        return "Generic spectrum classification ISP."

    @classmethod
    def domain_transfer_function(
            cls,
            input_domain: Type[DomainSpecifier]
    ) -> Type[DomainSpecifier]:
        from wai.annotations.domain.spectra.classification import SpectrumClassificationDomainSpecifier
        if input_domain is SpectrumClassificationDomainSpecifier:
            return input_domain
        else:
            raise Exception(
                f"Generic SC ISP only handles the following domains: "
                f"{SpectrumClassificationDomainSpecifier.name()}"
            )

    @classmethod
    def components(cls) -> Tuple[Type[ProcessorComponent]]:
        from wai.annotations.generic.isp.base.component import BaseISP
        return BaseISP,
