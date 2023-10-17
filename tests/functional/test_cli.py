"""Test the CLI commands."""

import pytest

@pytest.mark.parametrize('mock_strip', 'cli_test_client')
def test_initialize_database(cli_test_client, mock_strip):
    """Test the init_db command."""
    output = cli_test_client.invoke(args=["init_db"])
    assert output.exit_code == 0
    assert "Database initialized successfully!" in output.output
