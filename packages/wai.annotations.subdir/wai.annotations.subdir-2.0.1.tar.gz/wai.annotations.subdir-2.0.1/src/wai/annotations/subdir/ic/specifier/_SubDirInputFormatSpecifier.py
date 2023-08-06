from wai.annotations.domain.image.classification import ImageClassificationDomainSpecifier

from ...common.specifier import input_format_specifier


SubDirInputFormatSpecifier = input_format_specifier(ImageClassificationDomainSpecifier, "images")
