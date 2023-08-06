from typing import Type, Tuple

from wai.annotations.core.component import Component
from wai.annotations.core.domain import DomainSpecifier
from wai.annotations.core.specifier import SinkStageSpecifier


def output_format_specifier(
        domain_specifier: Type[DomainSpecifier],
        data_name_plural: str
) -> Type[SinkStageSpecifier]:
    class SubDirOutputFormatSpecifier(SinkStageSpecifier):
        """
        Specifier of the components for writing classification instances where
        each file is stored in a sub-directory named after the class label.
        """
        @classmethod
        def description(cls) -> str:
            return f"Writes {data_name_plural} to sub-directories named after their class labels."

        @classmethod
        def components(cls) -> Tuple[Type[Component], ...]:
            from ..component import SubDirWriter
            return SubDirWriter,

        @classmethod
        def domain(cls) -> Type[DomainSpecifier]:
            return domain_specifier

    return SubDirOutputFormatSpecifier
