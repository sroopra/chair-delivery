"""Floor plan parser module."""

import re
from collections import deque
from typing import Dict, List, Set, Tuple


class RoomParser:
    """Parser for extracting room information from floor plans."""

    def __init__(self, floor_plan: str):
        """Initialize the parser with a floor plan string.

        Args:
            floor_plan: String representation of the floor plan.
        """
        self.floor_plan = floor_plan
        self.grid: List[List[str]] = []
        self.rooms: Dict[str, Set[Tuple[int, int]]] = {}
        self.chair_types = {"W", "P", "S", "C"}

    def parse(self) -> Dict[str, Dict[str, int]]:
        """Parse the floor plan to extract room and chair information.

        Returns:
            A dictionary with room names as keys and chair counts as values.
        """
        if not self.floor_plan.strip():
            raise ValueError("Empty floor plan")

        # Step 1: Create a grid representation of the floor plan
        self._create_grid()

        # Step 2: Extract room names and their positions
        room_positions = self._extract_room_names()
        if not room_positions:
            raise ValueError("No room names found in floor plan")

        # Step 3: Map out each room's area using flood fill and return chairs
        return self._map_rooms(room_positions)
    

    def _create_grid(self) -> None:
        """Convert the floor plan string to a 2D grid."""
        self.grid = [list(line) for line in self.floor_plan.splitlines()]

    def _extract_room_names(self) -> Dict[str, Tuple[int, int]]:
        """Extract room names from the grid.

        Returns:
            Dictionary mapping room names to their positions (row, col).
        """
        room_positions = {}

        for row in range(len(self.grid)):
            line = "".join(self.grid[row])
            for match in re.finditer(r"\(([^)]+)\)", line):
                room_name = match.group(1).strip()
                # Find the position of the opening parenthesis
                col = match.start()
                # Store the room name and position
                room_positions[room_name] = (row, col)

        return room_positions

    def _map_rooms(self, room_positions: Dict[str, Tuple[int, int]]) -> Dict[str, Dict[str, int]]:
        """Map out each room's area and count chairs using flood fill algorithm.

        Args:
            room_positions: Dictionary mapping room names to positions.
        
        Returns:
            Dictionary with room names as keys and chair counts as values.
        """
        # Wall characters - used to determine room boundaries
        wall_chars = set(["|", "-", "+", "/", "\\"])

        # Track all visited coordinates to ensure rooms don't overlap
        all_visited = set()

        result = {}

        for room_name, (start_row, start_col) in room_positions.items():
            # Starting point for the room
            room_start = (start_row, start_col)

            # Create a set for this room's coordinates
            room_coords = set()
            chair_counts = {chair_type: 0 for chair_type in self.chair_types}

            # Perform a BFS flood fill to find all coordinates in the room
            queue = deque([room_start])
            visited = {room_start}

            while queue:
                r, c = queue.popleft()

                # Add to room coordinates
                room_coords.add((r, c))

                # Count chairs while doing flood fill
                if self.grid[r][c] in self.chair_types:
                    chair_counts[self.grid[r][c]] += 1

                # Check all adjacent cells (4-way adjacency)
                for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    nr, nc = r + dr, c + dc

                    if (
                        0 <= nr < len(self.grid)
                        and 0 <= nc < len(self.grid[nr])
                        and self.grid[nr][nc] not in wall_chars
                        and (nr, nc) not in visited
                        and (nr, nc) not in all_visited
                    ):
                        queue.append((nr, nc))
                        visited.add((nr, nc))

            # Save the room's coordinates and mark them as visited
            self.rooms[room_name] = room_coords
            all_visited.update(room_coords)
            result[room_name] = chair_counts

        return result
