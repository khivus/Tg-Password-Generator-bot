import enum


class GenerationType(enum.Enum):
    HUMAN = 'human'
    NON_HUMAN = 'non-human'


class SettingType(enum.Enum):
    COMPLEXITY = 'complexity'
    LENGTH = 'length'
    SEPARATOR = 'separator'
    USE_NUMBER = 'use_number'
    RESET = 'reset'
    USE_UPPER = 'use_upper'
    USE_LOWER = 'use_lower'
