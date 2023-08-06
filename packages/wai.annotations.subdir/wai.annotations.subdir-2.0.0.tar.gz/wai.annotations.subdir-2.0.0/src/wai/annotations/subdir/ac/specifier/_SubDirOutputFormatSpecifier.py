from wai.annotations.domain.audio.classification import AudioClassificationDomainSpecifier

from ...common.specifier import output_format_specifier

SubDirOutputFormatSpecifier = output_format_specifier(AudioClassificationDomainSpecifier, "audio files")
