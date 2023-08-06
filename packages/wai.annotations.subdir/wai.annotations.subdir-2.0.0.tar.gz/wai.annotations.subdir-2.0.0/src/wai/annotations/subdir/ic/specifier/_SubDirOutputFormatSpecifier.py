from wai.annotations.domain.image.classification import ImageClassificationDomainSpecifier

from ...common.specifier import output_format_specifier

SubDirOutputFormatSpecifier = output_format_specifier(ImageClassificationDomainSpecifier, "images")
