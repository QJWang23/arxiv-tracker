import sys
sys.path.insert(0, '.')

from filters.classifier import Classifier, classify_item


def test_classifier_init():
    clf = Classifier()
    assert "inference-opt" in clf.tag_keywords
    assert "quantization" in clf.tag_keywords["inference-opt"]


def test_classify_item():
    item = {
        "title": "Efficient Quantization for LLM Inference",
        "summary": "We propose a new quantization method for inference optimization."
    }
    tags = classify_item(item)
    assert "inference-opt" in tags


def test_classify_multimodal():
    item = {
        "title": "Multimodal Understanding with Vision Language Models",
        "summary": "A new approach to multimodal reasoning."
    }
    tags = classify_item(item)
    assert "multimodal" in tags


def test_classify_multiple_tags():
    item = {
        "title": "Long Context Multimodal Inference",
        "summary": "Handling long context in multimodal models with attention optimization."
    }
    tags = classify_item(item)
    assert "multimodal" in tags
    assert "long-context" in tags
