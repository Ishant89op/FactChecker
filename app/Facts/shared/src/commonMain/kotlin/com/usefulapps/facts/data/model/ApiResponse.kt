package com.usefulapps.facts.data.model

import kotlinx.serialization.Serializable

@Serializable
data class ApiResponse(
    val success: Boolean,
    val country: String,
    val keywords: List<String>,
    val numbers: List<String>,
    val phrases: List<String>,
    val found_on: Int,
    val total_checked: Int,
    val results: List<Result>? = null,
    val overall_verdict: String,
    val error: String? = null
)
