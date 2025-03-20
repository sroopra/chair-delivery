# Chair Count Automation Tool

Automates the counting of different chair types from floor plan text files.

## Installation

```bash
# Create a virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e ".[dev]"
```

## Usage

```bash
python -m chair_delivery.cli /path/to/floorplan.txt
```

## Development

```bash
# Run tests
pytest

# Format code
ruff format .

# Lint code
ruff check .
```