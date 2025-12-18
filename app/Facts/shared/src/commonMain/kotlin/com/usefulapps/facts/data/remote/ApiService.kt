package com.usefulapps.facts.data.remote

import com.usefulapps.facts.data.model.ApiRequest
import com.usefulapps.facts.data.model.ApiResponse
import io.ktor.client.HttpClient
import io.ktor.client.call.body
import io.ktor.client.request.get
import io.ktor.client.request.post
import io.ktor.client.request.setBody
import io.ktor.http.ContentType
import io.ktor.http.contentType

private val ApiURL = "http://localhost:8000/"
private val ApiVerifierURL = "http://localhost:8000/check"

class ApiService(
    private val client: HttpClient
) {
    suspend fun ApiDetails(): String {
        return client.get(ApiURL).body()
    }
    suspend fun runVerifierAPI(text: String): ApiResponse {
        println("POST API called")
        try {
            return client.post(ApiVerifierURL) {
                contentType(ContentType.Application.Json)
                setBody(ApiRequest(text))
            }.body()
        } catch (e: Exception) {
            println(e)
            throw e
        }
    }
}