"""
Integration test for the full pipeline.
Uses mock data to test the complete flow.
"""
import sys
import json
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from models import PaperItem
from filters.keyword_filter import filter_by_keywords
from filters.classifier import classify_item
from filters.scorer import HeatScorer


def test_full_pipeline():
    """Test the complete filtering pipeline."""
    # Create mock items
    items = [
        PaperItem(
            source="arxiv",
            id="2503.00001",
            title="Flash Attention 3: Fast Attention with Sparse Patterns",
            authors=["Tri Dao", "Author Two"],
            date="2026-03-26",
            url="https://arxiv.org/abs/2503.00001",
            summary="We present Flash Attention 3, a new approach to attention that achieves 2x speedup through sparse attention patterns and improved GPU utilization.",
            tags=[],
        ).to_dict(),
        PaperItem(
            source="arxiv",
            id="2503.00002",
            title="Efficient Quantization for Large Language Models",
            authors=["Some Author"],
            date="2026-03-26",
            url="https://arxiv.org/abs/2503.00002",
            summary="We propose a new quantization method that reduces memory usage by 4x while maintaining accuracy for inference optimization.",
            tags=[],
        ).to_dict(),
        PaperItem(
            source="arxiv",
            id="2503.00003",
            title="Generic Machine Learning Paper",
            authors=["Unknown Author"],
            date="2026-03-26",
            url="https://arxiv.org/abs/2503.00003",
            summary="A general overview of machine learning concepts.",
            tags=[],
        ).to_dict(),
    ]

    # Add realistic community/citation signals for scoring
    # Flash Attention: high citations + high HN score + author influence + tier1
    items[0]["citation_count"] = 100
    items[0]["hn_score"] = 500
    items[0]["author_influence"] = 0.5
    # Quantization paper: moderate signals
    items[1]["citation_count"] = 20
    items[1]["hn_score"] = 100

    # Step 1: Keyword filter
    filtered = filter_by_keywords(items)
    assert len(filtered) == 2  # Only first two match keywords

    # Step 2: Classify
    for item in filtered:
        tags = classify_item(item)
        item["tags"] = tags

    # Verify classification
    assert "inference-opt" in filtered[1]["tags"]  # Quantization paper

    # Step 3: Score
    scorer = HeatScorer()
    for item in filtered:
        scorer.score_item(item)

    # First paper should have higher score (tier1 critical keyword)
    assert filtered[0]["heat_score"] > filtered[1]["heat_score"]
    assert filtered[0]["priority"] == "critical"  # Flash attention

    # Step 4: Check instant push logic
    hot_items = [
        item for item in filtered
        if scorer.should_instant_push(item["heat_score"], item["priority"])
    ]
    assert len(hot_items) >= 1  # At least the Flash Attention paper


def test_save_and_load_filtered_data():
    """Test saving and loading filtered data."""
    items = [
        PaperItem(
            source="arxiv",
            id="2503.00001",
            title="Test Paper",
            authors=["Author"],
            date="2026-03-26",
            url="https://arxiv.org/abs/2503.00001",
            summary="Abstract",
            tags=["inference-opt"],
            heat_score=85,
            priority="high"
        ).to_dict()
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "test.json"
        path.write_text(json.dumps(items), encoding="utf-8")

        loaded = json.loads(path.read_text(encoding="utf-8"))
        assert len(loaded) == 1
        assert loaded[0]["id"] == "2503.00001"
