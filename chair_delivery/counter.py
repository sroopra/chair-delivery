"""Chair counter module."""

from typing import Dict

from .constants import CHAIR_TYPES


class ChairCounter:
    """Counter for chairs in a floor plan."""

    def __init__(self, room_data: Dict[str, Dict[str, int]]):
        """Initialize with parsed room data.

        Args:
            room_data: Dictionary mapping room names to chair counts.
        """
        self.room_data = room_data
        self.chair_types = CHAIR_TYPES  # Order for output

    def count_chairs(self) -> Dict[str, Dict[str, int]]:
        """Count chairs by type for each room and total.

        Returns:
            Dictionary with total and per-room chair counts.
        """
        result = {"total": {chair_type: 0 for chair_type in self.chair_types}}

        # Include all room data in the result
        for room_name, chair_counts in self.room_data.items():
            result[room_name] = chair_counts

            # Add to totals
            for chair_type, count in chair_counts.items():
                result["total"][chair_type] += count

        return result

    def format_output(self) -> str:
        """Format the chair counts as required by the legacy system.

        Returns:
            Formatted string with chair counts.
        """
        counts = self.count_chairs()
        lines = []

        # Format the total line
        lines.append("total:")
        lines.append(self._format_chair_counts(counts["total"]))

        # Format each room's lines, in alphabetical order
        for room_name in sorted(self.room_data.keys()):
            lines.append(f"{room_name}:")
            lines.append(self._format_chair_counts(counts[room_name]))

        return "\n".join(lines)

    def _format_chair_counts(self, counts: Dict[str, int]) -> str:
        """Format the counts for a single room or total.

        Args:
            counts: Dictionary mapping chair types to counts.

        Returns:
            Formatted string of counts.
        """
        parts = []
        for chair_type in self.chair_types:
            parts.append(f"{chair_type}: {counts[chair_type]}")

        return ", ".join(parts)
