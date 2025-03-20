"""Tests for the chair counter."""

from chair_delivery.counter import ChairCounter


def test_counter_initializes_with_room_data():
    """Test that the counter initializes correctly with room data."""
    room_data = {"room1": {"W": 1, "P": 2, "S": 0, "C": 0}}
    counter = ChairCounter(room_data)
    assert counter.room_data == room_data


def test_count_chairs_single_room():
    """Test that the counter correctly counts chairs for a single room."""
    room_data = {"room1": {"W": 1, "P": 2, "S": 0, "C": 0}}
    counter = ChairCounter(room_data)
    result = counter.count_chairs()

    assert "total" in result
    assert result["total"]["W"] == 1
    assert result["total"]["P"] == 2
    assert result["total"]["S"] == 0
    assert result["total"]["C"] == 0
    assert "room1" in result
    assert result["room1"] == room_data["room1"]


def test_count_chairs_multiple_rooms():
    """Test that the counter correctly counts chairs for multiple rooms."""
    room_data = {
        "room1": {"W": 1, "P": 2, "S": 0, "C": 0},
        "room2": {"W": 3, "P": 0, "S": 1, "C": 1},
    }
    counter = ChairCounter(room_data)
    result = counter.count_chairs()

    assert "total" in result
    assert result["total"]["W"] == 4
    assert result["total"]["P"] == 2
    assert result["total"]["S"] == 1
    assert result["total"]["C"] == 1
    assert "room1" in result
    assert "room2" in result
    assert result["room1"] == room_data["room1"]
    assert result["room2"] == room_data["room2"]


def test_count_chairs_empty_room():
    """Test that the counter handles a room with no chairs."""
    room_data = {
        "room1": {"W": 0, "P": 0, "S": 0, "C": 0},
        "room2": {"W": 1, "P": 1, "S": 1, "C": 1},
    }
    counter = ChairCounter(room_data)
    result = counter.count_chairs()

    assert "total" in result
    assert result["total"]["W"] == 1
    assert result["total"]["P"] == 1
    assert result["total"]["S"] == 1
    assert result["total"]["C"] == 1


def test_format_output_single_room():
    """Test that the counter correctly formats the output for a single room."""
    room_data = {"room1": {"W": 1, "P": 2, "S": 0, "C": 0}}
    counter = ChairCounter(room_data)
    result = counter.format_output()

    expected = "total:\nW: 1, P: 2, S: 0, C: 0\nroom1:\nW: 1, P: 2, S: 0, C: 0"
    assert result == expected


def test_format_output_multiple_rooms():
    """Test that the counter correctly formats the output for multiple rooms."""
    room_data = {
        "office": {"W": 1, "P": 2, "S": 0, "C": 0},
        "living room": {"W": 3, "P": 0, "S": 1, "C": 1},
    }
    counter = ChairCounter(room_data)
    result = counter.format_output()

    expected = (
        "total:\n"
        "W: 4, P: 2, S: 1, C: 1\n"
        "living room:\n"
        "W: 3, P: 0, S: 1, C: 1\n"
        "office:\n"
        "W: 1, P: 2, S: 0, C: 0"
    )
    assert result == expected


def test_format_output_alphabetical_order():
    """Test that the rooms are listed in alphabetical order in the output."""
    room_data = {
        "zebra": {"W": 1, "P": 0, "S": 0, "C": 0},
        "apple": {"W": 2, "P": 0, "S": 0, "C": 0},
        "banana": {"W": 3, "P": 0, "S": 0, "C": 0},
    }
    counter = ChairCounter(room_data)
    result = counter.format_output()

    # Check order of room names in output
    lines = result.split("\n")
    # Take every other line, starting from the first line (total:)
    room_lines = [lines[i] for i in range(0, len(lines), 2)]
    room_names = [line.strip(":") for line in room_lines]

    assert room_names == ["total", "apple", "banana", "zebra"]
