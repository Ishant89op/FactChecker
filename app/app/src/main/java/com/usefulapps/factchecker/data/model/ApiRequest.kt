package com.usefulapps.factchecker.data.model

import kotlinx.serialization.Serializable

@Serializable
data class VerificationRequest(
    val input: String,
    val type: String = "statement"  // "statement" or "url"
)
