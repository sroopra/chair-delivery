"""Integration tests for the chair delivery tool."""

from pathlib import Path

import pytest

from chair_delivery import cli
from chair_delivery.counter import ChairCounter
from chair_delivery.parser import RoomParser


def test_end_to_end_simple_floor_plan():
    """Test the end-to-end process with a simple floor plan."""
    # Create a simple floor plan with distinct vertical separator
    floor_plan = (
        "+-------------+-------------+\n"
        "| (living room)|(office)    |\n"
        "|   W W W     |   P P       |\n"
        "+-------------+-------------+"
    )

    # Process the floor plan
    parser = RoomParser(floor_plan)
    room_data = parser.parse()

    # Debug: Print the actual room data
    print("Parsed room data:", room_data)

    counter = ChairCounter(room_data)
    result = counter.format_output()

    expected = (
        "total:\n"
        "W: 3, P: 2, S: 0, C: 0\n"
        "living room:\n"
        "W: 3, P: 0, S: 0, C: 0\n"
        "office:\n"
        "W: 0, P: 2, S: 0, C: 0"
    )

    # Debug: Print the actual result
    print("Actual output:", result)
    print("Expected output:", expected)

    assert result == expected


def test_with_provided_rooms_file(monkeypatch, capsys):
    """Test with the provided rooms.txt file."""
    # Get the path to the rooms.txt file
    file_path = Path("rooms.txt")
    assert file_path.exists(), "rooms.txt file not found"

    # Invoke the CLI with the rooms.txt file
    monkeypatch.setattr("sys.argv", ["chair_delivery", str(file_path)])
    try:
        cli.main()
    except SystemExit:
        pass

    # Capture the output
    captured = capsys.readouterr()
    output = captured.out.strip()

    expected = (
        "total:\n"
        "W: 14, P: 7, S: 3, C: 1\n"
        "balcony:\n"
        "W: 0, P: 2, S: 0, C: 0\n"
        "bathroom:\n"
        "W: 0, P: 1, S: 0, C: 0\n"
        "closet:\n"
        "W: 0, P: 3, S: 0, C: 0\n"
        "kitchen:\n"
        "W: 4, P: 0, S: 0, C: 0\n"
        "living room:\n"
        "W: 7, P: 0, S: 2, C: 0\n"
        "office:\n"
        "W: 2, P: 1, S: 0, C: 0\n"
        "sleeping room:\n"
        "W: 1, P: 0, S: 1, C: 0\n"
        "toilet:\n"
        "W: 0, P: 0, S: 0, C: 1"
    )

    # Verify the expected output structure
    assert output.startswith("total:")
    assert "W:" in output
    assert "P:" in output
    assert "S:" in output
    assert "C:" in output
    # Check for at least some of the known rooms
    assert "living room:" in output
    assert "office:" in output
    assert "kitchen:" in output

    # Debug: Print the actual result
    print("Actual output:", output)
    print("Expected output:", expected)

    assert output == expected


@pytest.mark.parametrize(
    "file_content,expected_error",
    [
        ("", "error: empty floor plan"),
        ("Invalid content", "error parsing floor plan: no room names found"),
    ],
)
def test_cli_error_handling(
    file_content, expected_error, monkeypatch, capsys, tmp_path
):
    """Test CLI error handling with invalid inputs."""
    # Create a temporary file with invalid content
    temp_file = tmp_path / "invalid.txt"
    temp_file.write_text(file_content)

    # Mock sys.argv and sys.exit to prevent actual exit
    monkeypatch.setattr("sys.argv", ["chair_delivery", str(temp_file)])
    monkeypatch.setattr("sys.exit", lambda code: None)

    # Run the CLI with error handling
    try:
        cli.main()
    except Exception:
        # Ignore exceptions as they're expected
        pass

    # Check that error message is displayed
    captured = capsys.readouterr()
    # Convert to lowercase for case-insensitive comparison
    err_output = captured.err.lower()

    # Debug information
    print(f"Expected error: '{expected_error}'")
    print(f"Actual output: '{err_output}'")

    assert expected_error in err_output
