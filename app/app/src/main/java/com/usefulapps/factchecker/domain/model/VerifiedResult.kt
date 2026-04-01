package com.usefulapps.factchecker.domain.model

import com.usefulapps.factchecker.data.model.LLMVerdictData
import com.usefulapps.factchecker.data.model.SourceEvidenceData

data class VerifiedResult(
    val jobId: String,
    val finalVerdict: String,
    val finalScore: Int,
    val confidencePercent: Int,  // finalScore * 10
    val playwrightReasoning: String,
    val geminiReasoning: String?,
    val openaiReasoning: String?,
    val geminiVerdict: String?,
    val openaiVerdict: String?,
    val sources: List<SourceEvidenceData>,
    val modelsAgree: Boolean,
    val reconciliationNote: String,
    val originalClaim: String,
    val error: String? = null
)
