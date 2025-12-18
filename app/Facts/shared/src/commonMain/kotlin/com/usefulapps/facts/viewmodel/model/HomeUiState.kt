package com.usefulapps.facts.viewmodel.model

import com.usefulapps.facts.data.model.Result

data class HomeUiState(
    val input: String = "",
    val isLoading: Boolean = false,
    val isInputEnabled: Boolean = true,
    val isButtonEnabled: Boolean = true,
    val showResults: Boolean = false,
    val results: List<Result>? = null,
    val error: String? = null
)
