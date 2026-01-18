package com.usefulapps.factchecker.domain.model

import com.usefulapps.factchecker.data.model.Result

data class VerifiedResult(
    var success: Boolean,
    var found_on: Int,
    var total_checked: Int,
    var results: List<Result>? = null,
    var overall_verdict: String,
    var error: String? = null
)
