import os
from typing import Type, TypeVar

from wai.annotations.core.component.util import (
    LocalFileWriter,
    SplitSink,
    RequiresNoSplitFinalisation,
    SplitState,
    ExpectsDirectory
)
from wai.annotations.core.domain import Data, Instance
from wai.annotations.domain.classification import Classification

InstanceType = TypeVar('InstanceType', bound=Instance[Data, Classification])


class SubDirWriter(
    ExpectsDirectory,
    RequiresNoSplitFinalisation,
    LocalFileWriter[InstanceType],
    SplitSink[InstanceType]
):
    """
    Writes images into a separate sub-directory for each label.
    """
    _split_path = SplitState(lambda self: self.get_split_path(self.split_label, self.output))

    def consume_element_for_split(
            self,
            element: InstanceType
    ):
        # Format the class sub-directory
        class_path = self._split_path
        if element.annotations is not None:
            class_path = os.path.join(class_path, element.annotations.label)

        # Make sure the class sub-directory exists
        if not os.path.exists(class_path):
            os.mkdir(class_path)

        # Write the image to the class sub-directory
        element.data.write_data_if_present(class_path)

    @classmethod
    def get_help_text_for_output_option(cls) -> str:
        return "the directory to store the class directories in"
