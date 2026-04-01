CONTRADICTING_SIGNALS = [
    "false", "fake", "debunked", "misleading", "incorrect", "hoax",
    "myth", "fabricated", "disinformation", "misinformation", "conspiracy",
    "not true", "no evidence", "unproven", "unfounded", "baseless",
    "inaccurate", "wrong", "denied", "refuted", "retracted",
    "pants on fire", "four pinocchios", "mostly false",
]

SUPPORTING_SIGNALS = [
    "confirmed", "verified", "true", "accurate", "correct",
    "factual", "supported by evidence", "well-documented",
    "peer-reviewed", "established", "proven", "validated",
    "corroborated", "substantiated", "mostly true", "half true",
]


def detect_stance(text: str) -> str:
    text_lower = text.lower()

    contradict_count = 0
    for signal in CONTRADICTING_SIGNALS:
        if signal in text_lower:
            contradict_count += 1

    support_count = 0
    for signal in SUPPORTING_SIGNALS:
        if signal in text_lower:
            support_count += 1

    if contradict_count > support_count:
        return "contradicting"
    if support_count > contradict_count:
        return "supporting"
    return "neutral"
