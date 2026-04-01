package com.usefulapps.factchecker.data.model

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

// POST /verify response
@Serializable
data class VerifyResponse(
    @SerialName("job_id") val jobId: String,
    val status: String,
    val message: String
)

// GET /verify/{job_id}/status response
@Serializable
data class JobStatusResponse(
    @SerialName("job_id") val jobId: String,
    val status: String,
    @SerialName("sources_checked") val sourcesChecked: Int = 0,
    @SerialName("total_sources") val totalSources: Int = 0,
    val message: String = ""
)

// GET /verify/{job_id}/result response
@Serializable
data class JobResultResponse(
    @SerialName("job_id") val jobId: String,
    val request: RequestInfo? = null,
    val result: ReconciledResult? = null,
    val error: String? = null,
    val status: String? = null,
    val message: String? = null
)

@Serializable
data class RequestInfo(
    val input: String,
    val type: String
)

@Serializable
data class ReconciledResult(
    @SerialName("final_verdict") val finalVerdict: String,
    @SerialName("final_score") val finalScore: Int,
    @SerialName("playwright_score") val playwrightScore: PlaywrightScoreData,
    @SerialName("gemini_verdict") val geminiVerdict: LLMVerdictData? = null,
    @SerialName("openai_verdict") val openaiVerdict: LLMVerdictData? = null,
    val sources: List<SourceEvidenceData> = emptyList(),
    @SerialName("models_agree") val modelsAgree: Boolean,
    @SerialName("reconciliation_note") val reconciliationNote: String
)

@Serializable
data class PlaywrightScoreData(
    val score: Int,
    val reasoning: String,
    @SerialName("sources_used") val sourcesUsed: List<String> = emptyList()
)

@Serializable
data class LLMVerdictData(
    @SerialName("model_name") val modelName: String,
    val verdict: String,
    val score: Int,
    val reasoning: String,
    @SerialName("sources_used") val sourcesUsed: List<String> = emptyList()
)

@Serializable
data class SourceEvidenceData(
    @SerialName("source_name") val sourceName: String,
    val url: String,
    @SerialName("relevant_text") val relevantText: String,
    val stance: String
)

// GET /history response
@Serializable
data class HistoryResponse(
    val items: List<HistoryItem>,
    @SerialName("next_cursor") val nextCursor: String = ""
)

@Serializable
data class HistoryItem(
    @SerialName("job_id") val jobId: String,
    val input: String,
    val type: String = "statement",
    @SerialName("final_score") val finalScore: Int? = null,
    @SerialName("final_verdict") val finalVerdict: String? = null
)

// GET /health response
@Serializable
data class HealthResponse(
    val status: String
)
