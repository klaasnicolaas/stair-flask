"""Exceptions for Stair Challenge."""


class StairChallengeControlError(Exception):
    """Generic Stair Challenge exception."""


class StairChallengeConnectionError(StairChallengeControlError):
    """Stair Challenge connection exception."""
