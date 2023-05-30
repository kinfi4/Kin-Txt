from enum import Enum

PROJECT_TITLE = 'Kin-News'
PROJECT_DESCRIPTION = 'Kin-News is a service for storing user subscriptions, retrieving news messages, storing user ratings.'

DELETED_CHANNEL_TITLE = 'This Channel was deleted, or channel link has changed'

class PossibleRating(int, Enum):
    ZERO = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
