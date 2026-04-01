package com.usefulapps.factchecker.data.remote

import com.usefulapps.factchecker.data.model.*
import io.ktor.client.HttpClient
import io.ktor.client.call.body
import io.ktor.client.request.get
import io.ktor.client.request.header
import io.ktor.client.request.post
import io.ktor.client.request.setBody
import io.ktor.http.ContentType
import io.ktor.http.contentType

class ApiService(
    private val client: HttpClient
) {
    private val baseUrl get() = HTTPclient.baseUrl

    /** POST /verify — starts a verification job */
    suspend fun startVerification(input: String, type: String = "statement", firebaseToken: String): VerifyResponse {
        return client.post("$baseUrl/verify") {
            contentType(ContentType.Application.Json)
            header("Authorization", "Bearer $firebaseToken")
            setBody(VerificationRequest(input, type))
        }.body()
    }

    /** GET /verify/{jobId}/status — polls job status */
    suspend fun getJobStatus(jobId: String, firebaseToken: String): JobStatusResponse {
        return client.get("$baseUrl/verify/$jobId/status") {
            header("Authorization", "Bearer $firebaseToken")
        }.body()
    }

    /** GET /verify/{jobId}/result — gets the final result */
    suspend fun getJobResult(jobId: String, firebaseToken: String): JobResultResponse {
        return client.get("$baseUrl/verify/$jobId/result") {
            header("Authorization", "Bearer $firebaseToken")
        }.body()
    }

    /** GET /history — paginated verification history */
    suspend fun getHistory(firebaseToken: String, limit: Int = 20, cursor: String = ""): HistoryResponse {
        val cursorParam = if (cursor.isNotEmpty()) "&cursor=$cursor" else ""
        return client.get("$baseUrl/history?limit=$limit$cursorParam") {
            header("Authorization", "Bearer $firebaseToken")
        }.body()
    }

    /** GET /health — server health check */
    suspend fun checkHealth(): HealthResponse {
        return client.get("$baseUrl/health").body()
    }
}