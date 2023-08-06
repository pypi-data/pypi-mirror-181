import os
from typing import Type, TypeVar

from wai.annotations.core.component.util import AnnotationFileProcessor
from wai.annotations.core.domain import Data, Instance
from wai.annotations.core.stream import ThenFunction
from wai.annotations.domain.classification import Classification

InstanceType = TypeVar('InstanceType', bound=Instance[Data, Classification])


def reader_class(instance_type: Type[InstanceType]) -> Type[AnnotationFileProcessor[InstanceType]]:
    class SubDirReader(AnnotationFileProcessor[InstanceType]):
        """
        Reader of classification datasets which store files in
        folders named after the classification label.
        """
        def read_annotation_file(self, filename: str, then: ThenFunction[InstanceType]):
            # The label is the last directory folder of the filename
            label = os.path.basename(os.path.dirname(filename))

            then(
                instance_type(
                    instance_type.data_type().from_file(filename),
                    Classification(label)
                )
            )

        def read_negative_file(self, filename: str, then: ThenFunction[InstanceType]):
            then(
                instance_type(
                    instance_type.data_type().from_file(filename),
                    None
                )
            )

    return SubDirReader
