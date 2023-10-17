"""Test the CLI commands."""


def test_initialize_database(cli_test_client):
    """Test the init_db command."""
    output = cli_test_client.invoke(args=["init_db"])
    assert output.exit_code == 0
    assert "Database initialized successfully!" in output.output
