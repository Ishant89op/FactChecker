from typing import Optional

from core3.models import (
    PlaywrightScore,
    LLMVerdict,
    ReconciledResult,
    SourceEvidence,
)


def reconcile(
    playwright_score: PlaywrightScore,
    gemini_verdict: Optional[LLMVerdict],
    openai_verdict: Optional[LLMVerdict],
    sources: list[SourceEvidence],
) -> ReconciledResult:
    available_scores = [playwright_score.score]
    unavailable = []

    if gemini_verdict:
        available_scores.append(gemini_verdict.score)
    else:
        unavailable.append("Gemini")

    if openai_verdict:
        available_scores.append(openai_verdict.score)
    else:
        unavailable.append("OpenAI")

    final_score = min(available_scores)

    if final_score >= 8:
        final_verdict = "VERY_LIKELY"
    elif final_score >= 6:
        final_verdict = "LIKELY"
    elif final_score >= 4:
        final_verdict = "UNLIKELY"
    else:
        final_verdict = "VERY_UNLIKELY"

    models_agree = True
    if gemini_verdict and openai_verdict:
        if gemini_verdict.verdict != openai_verdict.verdict:
            models_agree = False
            final_verdict = "DISPUTED"

    note_parts = []
    note_parts.append(f"Playwright engine scored {playwright_score.score}/10.")

    if gemini_verdict:
        note_parts.append(
            f"Gemini scored {gemini_verdict.score}/10 ({gemini_verdict.verdict})."
        )
    if openai_verdict:
        note_parts.append(
            f"OpenAI scored {openai_verdict.score}/10 ({openai_verdict.verdict})."
        )

    if unavailable:
        note_parts.append(
            f"{', '.join(unavailable)} was unavailable and excluded from scoring."
        )

    if not models_agree:
        note_parts.append(
            "Gemini and OpenAI reached different verdicts. Marking as DISPUTED."
        )

    note_parts.append(f"Final score: {final_score}/10. Verdict: {final_verdict}.")

    return ReconciledResult(
        final_verdict=final_verdict,
        final_score=final_score,
        playwright_score=playwright_score,
        gemini_verdict=gemini_verdict,
        openai_verdict=openai_verdict,
        sources=sources,
        models_agree=models_agree,
        reconciliation_note=" ".join(note_parts),
    )
