package com.usefulapps.factchecker.data.remote

import io.ktor.client.HttpClient
import io.ktor.client.engine.okhttp.OkHttp
import io.ktor.client.plugins.contentnegotiation.ContentNegotiation
import io.ktor.client.plugins.defaultRequest
import io.ktor.serialization.kotlinx.json.json
import kotlinx.serialization.json.Json

object HTTPclient {
    // Set these before creating the client, or hardcode for dev
    var baseUrl: String = "http://10.0.2.2:8000"  // Android emulator → host localhost
    var apiKey: String = ""

    fun create(): HttpClient =
        HttpClient(OkHttp) {
            install(ContentNegotiation) {
                json(
                    Json {
                        ignoreUnknownKeys = true
                        isLenient = true
                    }
                )
            }

            defaultRequest {
                if (apiKey.isNotEmpty()) {
                    headers.append("X-API-Key", apiKey)
                }
            }
        }
}