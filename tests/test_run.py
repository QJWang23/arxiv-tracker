import sys
import json
import tempfile
from pathlib import Path

sys.path.insert(0, '.')

from run import load_filtered_data, filter_hot_items


def test_load_filtered_data(tmp_path):
    # Create test data
    data_file = tmp_path / "2026-03-26.json"
    data = [{"id": "1", "title": "Test", "heat_score": 85, "priority": "high"}]
    data_file.write_text(json.dumps(data))

    items = load_filtered_data(data_file)
    assert len(items) == 1
    assert items[0]["id"] == "1"


def test_filter_hot_items():
    items = [
        {"id": "1", "heat_score": 85, "priority": "high"},
        {"id": "2", "heat_score": 70, "priority": "high"},
        {"id": "3", "heat_score": 90, "priority": "normal"},
        {"id": "4", "heat_score": 95, "priority": "critical"},
    ]
    hot = filter_hot_items(items)
    assert len(hot) == 2
    assert hot[0]["id"] == "4"  # critical with high score first
    assert hot[1]["id"] == "1"  # high with score > 80