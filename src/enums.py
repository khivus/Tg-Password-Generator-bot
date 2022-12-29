import enum


class GenerationType(enum.Enum):
    HUMAN = 'human'
    NON_HUMAN = 'non-human'
    NUMBERS_ONLY = 'numbers-only'


class SettingType(enum.Enum):
    COMPLEXITY = 'complexity'
    SEPARATOR = 'separator'
    USE_NUMBER = 'use_number'
    RESET = 'reset'
