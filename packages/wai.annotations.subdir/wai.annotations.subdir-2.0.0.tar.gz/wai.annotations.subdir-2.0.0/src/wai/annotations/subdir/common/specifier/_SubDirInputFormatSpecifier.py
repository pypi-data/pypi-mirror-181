from typing import Type, Tuple

from wai.annotations.core.component import Component
from wai.annotations.core.domain import DomainSpecifier
from wai.annotations.core.specifier import SourceStageSpecifier


def input_format_specifier(
        domain_specifier: Type[DomainSpecifier],
        data_name_plural: str
) -> Type[SourceStageSpecifier]:
    class SubDirInputFormatSpecifier(SourceStageSpecifier):
        """
        Specifier of the components for reading classification instances where
        each file is stored in a sub-directory named after the class label.
        """
        @classmethod
        def description(cls) -> str:
            return f"Reads {data_name_plural} from sub-directories named after their class labels."

        @classmethod
        def components(cls) -> Tuple[Type[Component], ...]:
            from wai.annotations.core.component.util import LocalFilenameSource
            from ..component import reader_class
            return LocalFilenameSource, reader_class(domain_specifier.instance_type())

        @classmethod
        def domain(cls) -> Type[DomainSpecifier]:
            return domain_specifier

    return SubDirInputFormatSpecifier
