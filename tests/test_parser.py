"""Tests for the floor plan parser."""

from chair_delivery.parser import RoomParser


def test_parser_initializes_with_floor_plan():
    """Test that the parser initializes correctly with a floor plan."""
    floor_plan = "Example floor plan"
    parser = RoomParser(floor_plan)
    assert parser.floor_plan == floor_plan
    assert parser.grid == []
    assert parser.rooms == {}
    assert parser.chair_types == {"W", "P", "S", "C"}


def test_create_grid_from_floor_plan():
    """Test that the parser correctly creates a grid from the floor plan."""
    floor_plan = "+-+\n|W|\n+-+"

    parser = RoomParser(floor_plan)
    parser._create_grid()

    assert parser.grid == [["+", "-", "+"], ["|", "W", "|"], ["+", "-", "+"]]


def test_extract_room_names():
    """Test that the parser extracts room names."""
    floor_plan = "+----------+\n| (room1)  |\n+----------+\n| (room2)  |\n+----------+"

    parser = RoomParser(floor_plan)
    parser._create_grid()
    room_positions = parser._extract_room_names()

    assert "room1" in room_positions
    assert "room2" in room_positions

    # Check positions
    assert isinstance(room_positions["room1"], tuple)
    assert isinstance(room_positions["room2"], tuple)


def test_map_rooms_with_flood_fill():
    """Test that the parser maps rooms using flood fill."""
    floor_plan = "+-----+\n|(room)|\n|  W   |\n+-----+"

    parser = RoomParser(floor_plan)
    parser._create_grid()
    room_positions = parser._extract_room_names()
    parser._map_rooms(room_positions)

    assert "room" in parser.rooms
    assert len(parser.rooms["room"]) > 0
    # Verify a specific position in the room
    assert (2, 3) in parser.rooms["room"]  # Position of the W chair


def test_count_chairs_in_rooms():
    """Test that the parser correctly counts chairs in rooms."""
    floor_plan = "+-----+\n|(room)|\n|W P S|\n+-----+"

    parser = RoomParser(floor_plan)
    result = parser.parse()

    assert "room" in result
    assert result["room"]["W"] == 1
    assert result["room"]["P"] == 1
    assert result["room"]["S"] == 1
    assert result["room"]["C"] == 0


def test_handle_multiple_rooms():
    """Test that the parser handles multiple rooms."""
    floor_plan = "+-----+-----+\n|(room1)|(room2)|\n|W P   |S C   |\n+-----+-----+"

    parser = RoomParser(floor_plan)
    result = parser.parse()

    assert "room1" in result
    assert "room2" in result
    assert result["room1"]["W"] == 1
    assert result["room1"]["P"] == 1
    assert result["room1"]["S"] == 0
    assert result["room1"]["C"] == 0
    assert result["room2"]["W"] == 0
    assert result["room2"]["P"] == 0
    assert result["room2"]["S"] == 1
    assert result["room2"]["C"] == 1
