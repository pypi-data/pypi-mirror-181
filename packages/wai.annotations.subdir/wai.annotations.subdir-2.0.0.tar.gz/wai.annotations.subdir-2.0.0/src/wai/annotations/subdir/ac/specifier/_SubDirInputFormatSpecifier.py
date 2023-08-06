from wai.annotations.domain.audio.classification import AudioClassificationDomainSpecifier

from ...common.specifier import input_format_specifier


SubDirInputFormatSpecifier = input_format_specifier(AudioClassificationDomainSpecifier, "audio files")
