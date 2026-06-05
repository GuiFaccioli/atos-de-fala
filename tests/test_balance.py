from chomsky.gen.balance import act_counts, under_target_acts
from chomsky.schema import Annotation, Span


def test_act_counts_sums_spans_per_act():
    anns = [
        Annotation("a", [Span(0, 1, "informar"), Span(1, 2, "pedir")]),
        Annotation("b", [Span(0, 1, "informar")]),
    ]
    assert act_counts(anns) == {"informar": 2, "pedir": 1}


def test_under_target_returns_lowest_below_target():
    acts = ["informar", "pedir", "sugerir", "oferecer"]
    counts = {"informar": 10, "pedir": 1, "sugerir": 0}  # oferecer missing -> 0
    # target 5: below = pedir(1), sugerir(0), oferecer(0); lowest first, tie by acts order
    assert under_target_acts(counts, acts, target=5, k=3) == ["sugerir", "oferecer", "pedir"]


def test_under_target_caps_at_k():
    acts = ["a", "b", "c", "d"]
    assert under_target_acts({}, acts, target=1, k=2) == ["a", "b"]


def test_under_target_empty_when_all_met():
    acts = ["a", "b"]
    assert under_target_acts({"a": 5, "b": 5}, acts, target=5, k=3) == []
