"""Test the CLI commands."""

from app.led_controller import LEDController

def test_initialize_database(cli_test_client, mock_strip):
    """Test the init_db command."""
    controller = LEDController(
        count=mock_strip.numPixels(),
        pin=18,
        freq_hz=800000,
        dma=10,
        invert=False,
        brightness=255,
        channel=0,
    )
    controller.start()

    output = cli_test_client.invoke(args=["init_db"])
    assert output.exit_code == 0
    assert "Database initialized successfully!" in output.output
