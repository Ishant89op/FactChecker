package com.usefulapps.factchecker.data.model

import kotlinx.serialization.Serializable

@Serializable
data class ApiRequest(
    val text: String
)
