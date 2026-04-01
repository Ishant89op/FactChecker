from core3.models import SourceEvidence, PlaywrightScore


TIER_WEIGHTS = {
    1: 3.0,
    2: 2.0,
    3: 1.0,
}

SOURCE_TIERS = {
    "Wikipedia": 1,
    "Reuters Fact Check": 1,
    "AP Fact Check": 1,
    "WHO": 1,
    "CDC": 1,
    "Snopes": 2,
    "FactCheck.org": 2,
    "PolitiFact": 2,
    "Google": 3,
    "ScienceDirect": 3,
}


def compute_score(evidence: list[SourceEvidence]) -> PlaywrightScore:
    if not evidence:
        return PlaywrightScore(
            score=5,
            reasoning="No sources returned useful evidence. Defaulting to neutral.",
            sources_used=[],
        )

    weighted_sum = 0.0
    total_weight = 0.0
    sources_used = []

    for item in evidence:
        tier = SOURCE_TIERS.get(item.source_name, 3)
        weight = TIER_WEIGHTS.get(tier, 1.0)

        if item.stance == "supporting":
            weighted_sum += weight * 1.0
        elif item.stance == "contradicting":
            weighted_sum += weight * -1.0

        total_weight += weight
        sources_used.append(item.source_name)

    if total_weight == 0:
        raw_score = 5.0
    else:
        normalized = weighted_sum / total_weight
        raw_score = 5.0 + (normalized * 5.0)

    final_score = max(1, min(10, round(raw_score)))

    supporting = [e for e in evidence if e.stance == "supporting"]
    contradicting = [e for e in evidence if e.stance == "contradicting"]
    neutral = [e for e in evidence if e.stance == "neutral"]

    reasoning = (
        f"Checked {len(evidence)} sources. "
        f"{len(supporting)} supporting, "
        f"{len(contradicting)} contradicting, "
        f"{len(neutral)} neutral. "
        f"Weighted score: {final_score}/10."
    )

    return PlaywrightScore(
        score=final_score,
        reasoning=reasoning,
        sources_used=sources_used,
    )
