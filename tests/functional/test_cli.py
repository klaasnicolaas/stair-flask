"""Test the CLI commands."""

import pytest


def test_initialize_database(cli_test_client: pytest.fixture) -> None:
    """Test the init_db command.

    Args:
    ----
        cli_test_client: Test client for the Flask application
    """
    output = cli_test_client.invoke(args=["init_db"])
    assert output.exit_code == 0
    assert "Database initialized successfully!" in output.output
