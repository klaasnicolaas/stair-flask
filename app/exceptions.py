"""Exceptions for Stair Challenge."""


class StairChallengeControlError(Exception):
    """Generic Stair Challenge exception."""


class StairChallengeConnectionError(StairChallengeControlError):
    """Stair Challenge connection exception."""


class StairChalllengeInitializationError(StairChallengeControlError):
    """Stair Challenge initialization exception."""


class StairChallengeMQTTConnectionError(StairChallengeControlError):
    """Stair Challenge MQTT connection exception."""

    def __init__(self, host: str) -> None:
        """Init MQTT connection error.

        Args:
        ----
            host: MQTT Broker host.
        """
        super().__init__(f"Could not connect to MQTT Broker at {host}.")
