package com.usefulapps.factchecker.viewmodel.model

import com.usefulapps.factchecker.data.model.Result

data class HomeUiState(
    val input: String = "",
    val isLoading: Boolean = false,
    val isInputEnabled: Boolean = true,
    val isCheckButtonEnabled: Boolean = true,
    val isGetInfoButtonEnabled: Boolean = true,
    val showResults: Boolean = false,
    val results: List<Result>? = null,
    val error: String? = null
)
