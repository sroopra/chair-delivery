"""Command line interface for the chair delivery tool."""

import argparse
import sys
from pathlib import Path

from chair_delivery.counter import ChairCounter
from chair_delivery.parser import RoomParser


def main():
    """Entry point for the chair delivery tool."""
    parser = argparse.ArgumentParser(description="Count chairs in floor plans")
    parser.add_argument("file_path", type=str, help="Path to the floor plan text file")

    args = parser.parse_args()
    file_path = Path(args.file_path)

    if not file_path.exists():
        print(f"Error: File {file_path} does not exist", file=sys.stderr)
        sys.exit(1)

    room_data = None

    try:
        # Read the floor plan file
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                floor_plan = f.read()
        except Exception as e:
            print(f"Error reading file: {e}", file=sys.stderr)
            sys.exit(1)

        # Check if the file is empty
        if not floor_plan.strip():
            print("Error: Empty floor plan", file=sys.stderr)
            sys.exit(1)

        # Parse the floor plan
        try:
            room_parser = RoomParser(floor_plan)
            room_data = room_parser.parse()
        except ValueError as e:
            print(f"Error parsing floor plan: {e}", file=sys.stderr)
            sys.exit(1)

        # Count and format the results
        if room_data:
            chair_counter = ChairCounter(room_data)
            result = chair_counter.format_output()
            print(result)
        else:
            print("Error: No rooms found in floor plan", file=sys.stderr)
            sys.exit(1)

    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
