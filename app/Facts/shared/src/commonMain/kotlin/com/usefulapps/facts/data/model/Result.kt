package com.usefulapps.facts.data.model

import io.ktor.http.Url
import kotlinx.serialization.Serializable

@Serializable
data class Result(
    val found: Boolean,
    val site: String,
    val url: String,
    val snippet: String,
    val numbers_matched: Int,
    val phrases_matched: Int,
    val verdict: Boolean,
    val error: String? = null
)
