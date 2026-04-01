package com.usefulapps.factchecker.domain.repository

import com.usefulapps.factchecker.data.model.HistoryItem
import com.usefulapps.factchecker.data.remote.ApiService
import com.usefulapps.factchecker.domain.model.VerifiedResult
import kotlinx.coroutines.delay

class CheckerRepository(
    private val apiService: ApiService
) {
    private var firebaseToken: String = ""

    fun setFirebaseToken(token: String) {
        firebaseToken = token
    }

    suspend fun isServiceOnline(): Boolean {
        return try {
            val response = apiService.checkHealth()
            response.status == "ok"
        } catch (e: Exception) {
            false
        }
    }

    /**
     * Starts verification, polls for completion, returns final result.
     * Calls onStatusUpdate with each poll so the UI can show progress.
     */
    suspend fun verify(
        input: String,
        type: String = "statement",
        onStatusUpdate: (status: String, message: String, sourcesChecked: Int) -> Unit = { _, _, _ -> }
    ): VerifiedResult {
        // 1. Start the job
        val verifyResponse = apiService.startVerification(input, type, firebaseToken)
        val jobId = verifyResponse.jobId

        // 2. Poll until complete or failed
        var attempts = 0
        val maxAttempts = 120  // 2 minutes at 1s intervals
        while (attempts < maxAttempts) {
            delay(1000)
            attempts++

            val statusResponse = apiService.getJobStatus(jobId, firebaseToken)
            onStatusUpdate(statusResponse.status, statusResponse.message, statusResponse.sourcesChecked)

            when (statusResponse.status) {
                "complete" -> break
                "failed" -> {
                    return VerifiedResult(
                        jobId = jobId,
                        finalVerdict = "FAILED",
                        finalScore = 0,
                        confidencePercent = 0,
                        playwrightReasoning = "",
                        geminiReasoning = null,
                        openaiReasoning = null,
                        geminiVerdict = null,
                        openaiVerdict = null,
                        sources = emptyList(),
                        modelsAgree = false,
                        reconciliationNote = "",
                        originalClaim = input,
                        error = statusResponse.message
                    )
                }
            }
        }

        // 3. Fetch the full result
        val resultResponse = apiService.getJobResult(jobId, firebaseToken)
        val result = resultResponse.result

        if (result == null) {
            return VerifiedResult(
                jobId = jobId,
                finalVerdict = "ERROR",
                finalScore = 0,
                confidencePercent = 0,
                playwrightReasoning = "",
                geminiReasoning = null,
                openaiReasoning = null,
                geminiVerdict = null,
                openaiVerdict = null,
                sources = emptyList(),
                modelsAgree = false,
                reconciliationNote = "",
                originalClaim = input,
                error = resultResponse.error ?: "Could not retrieve result"
            )
        }

        return VerifiedResult(
            jobId = jobId,
            finalVerdict = result.finalVerdict,
            finalScore = result.finalScore,
            confidencePercent = result.finalScore * 10,
            playwrightReasoning = result.playwrightScore.reasoning,
            geminiReasoning = result.geminiVerdict?.reasoning,
            openaiReasoning = result.openaiVerdict?.reasoning,
            geminiVerdict = result.geminiVerdict?.verdict,
            openaiVerdict = result.openaiVerdict?.verdict,
            sources = result.sources,
            modelsAgree = result.modelsAgree,
            reconciliationNote = result.reconciliationNote,
            originalClaim = input
        )
    }

    suspend fun getHistory(cursor: String = ""): Pair<List<HistoryItem>, String> {
        val response = apiService.getHistory(firebaseToken, cursor = cursor)
        return Pair(response.items, response.nextCursor)
    }
}