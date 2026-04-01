import asyncio
import json
import logging
from typing import Optional

import google.generativeai as genai
from openai import AsyncOpenAI

from core3.models import SourceEvidence, LLMVerdict

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "You are a fact-checking analyst. You will receive a claim and scraped evidence "
    "from multiple sources. Analyze the evidence and determine whether the claim is "
    "likely true or false. Respond ONLY with valid JSON matching this exact schema, "
    "no extra text before or after:\n"
    '{"verdict": "TRUE|FALSE|MISLEADING|UNVERIFIABLE", '
    '"score": <integer 1-10 where 1=very unlikely true, 10=very likely true>, '
    '"reasoning": "<2-3 sentence explanation>", '
    '"sources_used": ["<url1>", "<url2>"]}'
)

EVIDENCE_CAP = 6000


def _build_prompt(claim: str, evidence: list[SourceEvidence]) -> str:
    parts = [f"CLAIM: {claim}\n\nEVIDENCE:\n"]
    char_count = len(parts[0])

    for item in evidence:
        entry = (
            f"- Source: {item.source_name}\n"
            f"  URL: {item.url}\n"
            f"  Stance: {item.stance}\n"
            f"  Text: {item.relevant_text}\n\n"
        )
        if char_count + len(entry) > EVIDENCE_CAP:
            break
        parts.append(entry)
        char_count += len(entry)

    if len(parts) == 1:
        parts.append("No evidence was found from any source.\n")

    parts.append(
        "Based on the above evidence, score this claim from 1 (very unlikely true) "
        "to 10 (very likely true). Provide your verdict, score, reasoning, and "
        "which source URLs informed your decision."
    )

    return "".join(parts)


def _parse_llm_response(raw: str, model_name: str) -> Optional[LLMVerdict]:
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        lines = cleaned.split("\n")
        lines = [l for l in lines if not l.strip().startswith("```")]
        cleaned = "\n".join(lines)

    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        logger.warning(f"{model_name}: failed to parse JSON response")
        return None

    verdict = data.get("verdict", "UNVERIFIABLE").upper()
    valid_verdicts = {"TRUE", "FALSE", "MISLEADING", "UNVERIFIABLE"}
    if verdict not in valid_verdicts:
        verdict = "UNVERIFIABLE"

    score = data.get("score", 5)
    if not isinstance(score, int):
        try:
            score = int(score)
        except (ValueError, TypeError):
            score = 5
    score = max(1, min(10, score))

    return LLMVerdict(
        model_name=model_name,
        verdict=verdict,
        score=score,
        reasoning=data.get("reasoning", "No reasoning provided."),
        sources_used=data.get("sources_used", []),
    )


async def query_gemini(
    claim: str,
    evidence: list[SourceEvidence],
    api_key: str,
    model_name: str = "gemini-1.5-flash",
) -> Optional[LLMVerdict]:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        prompt = _build_prompt(claim, evidence)
        full_prompt = f"{SYSTEM_PROMPT}\n\n{prompt}"

        response = await asyncio.to_thread(
            model.generate_content, full_prompt
        )

        raw = response.text
        return _parse_llm_response(raw, "gemini")

    except Exception as e:
        logger.error(f"Gemini query failed: {str(e)[:200]}")
        return None


async def query_openai(
    claim: str,
    evidence: list[SourceEvidence],
    api_key: str,
    model_name: str = "gpt-4o-mini",
) -> Optional[LLMVerdict]:
    try:
        client = AsyncOpenAI(api_key=api_key)
        prompt = _build_prompt(claim, evidence)

        response = await client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.1,
            max_tokens=500,
        )

        raw = response.choices[0].message.content
        return _parse_llm_response(raw, "openai")

    except Exception as e:
        logger.error(f"OpenAI query failed: {str(e)[:200]}")
        return None


async def run_llm_engines(
    claim: str,
    evidence: list[SourceEvidence],
    gemini_api_key: str,
    openai_api_key: str,
    gemini_model: str = "gemini-1.5-flash",
    openai_model: str = "gpt-4o-mini",
) -> tuple[Optional[LLMVerdict], Optional[LLMVerdict]]:
    gemini_task = query_gemini(claim, evidence, gemini_api_key, gemini_model)
    openai_task = query_openai(claim, evidence, openai_api_key, openai_model)

    results = await asyncio.gather(gemini_task, openai_task, return_exceptions=True)

    gemini_result = results[0] if not isinstance(results[0], Exception) else None
    openai_result = results[1] if not isinstance(results[1], Exception) else None

    if isinstance(results[0], Exception):
        logger.error(f"Gemini raised exception: {results[0]}")
    if isinstance(results[1], Exception):
        logger.error(f"OpenAI raised exception: {results[1]}")

    return gemini_result, openai_result
